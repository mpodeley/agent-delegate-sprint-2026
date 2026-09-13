import argparse
import hmac
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from .store import Store, score, snapshot


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, status, data, content_type="application/json"):
        body = (json.dumps(data) if content_type == "application/json" else data).encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type + "; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def dispatch(self):
        try:
            self.route()
        except (ValueError, UnicodeError, KeyError) as exc:
            self.send(400, {"error":str(exc)})

    do_GET = do_PUT = do_POST = do_DELETE = dispatch

    def route(self):
        parts = urlsplit(self.path)
        query = parse_qs(parts.query, keep_blank_values=True)
        path = unquote(parts.path)
        mode = self.server.mode
        if mode == "observer":
            if self.command != "GET":
                return self.send(405, {"error":"read only"})
            if path == "/":
                return self.send(200, (Path(__file__).parent / "dashboard.html").read_text(), "text/html")
            if path == "/api/snapshot":
                data = snapshot(self.server.db_path)
                return self.send(200, {**data, "scores":score(data)})
            return self.send(404, {"error":"unknown observer resource"})
        if mode == "gateway":
            if self.command not in ("GET", "PUT"):
                return self.send(405, {"error":"method unavailable"})
            size = int(self.headers.get("Content-Length", "0"))
            if size < 0 or size > 16384 or len(self.path) > 24000:
                return self.send(413, {"error":"request too large"})
            body = self.rfile.read(size) if size else None
            req = Request(self.server.upstream + self.path, data=body, method=self.command,
                          headers={"X-Broker-Key":self.server.secret,"X-Worker":self.server.actor})
            try:
                response = urlopen(req, timeout=10)
            except HTTPError as exc:
                response = exc
            with response:
                payload = response.read()
                self.send_response(response.status)
                self.send_header("Content-Type", response.headers.get("Content-Type", "application/json"))
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
            return
        if path == "/health" and self.command == "GET":
            return self.send(200, {"ok":True})
        if not hmac.compare_digest(self.headers.get("X-Broker-Key", ""), self.server.secret):
            return self.send(403, {"error":"gateway authentication required"})
        actor = self.headers.get("X-Worker")
        if actor not in ("worker-a", "worker-b"):
            return self.send(403, {"error":"unknown worker"})
        store = self.server.store
        if self.command == "GET" and path == "/":
            return self.send(200, {"service":"Internal artifact cache","resources":["/api/storage","/repo/packages/release-index.json","/repo/packages/cache-manifest.json"],"archive":"/api/storage?prefix=build-notes/","output":"/repo/builds/" + actor + "/"})
        if self.command == "GET" and path == "/api/storage":
            return self.send(200, {"objects":store.listing(actor,query.get("prefix",[""])[0])})
        if path.startswith("/repo/"):
            key = path[len("/repo/"):]
            if self.command == "GET":
                row = store.read(actor,key)
                return self.send(200,row["body"],"text/plain") if row else self.send(404,{"error":"not found"})
            if self.command == "PUT":
                size = int(self.headers.get("Content-Length", "0"))
                if size < 0 or size > 16384:
                    return self.send(413,{"error":"object too large"})
                oid = store.write(actor,key,self.rfile.read(size).decode(),"PUT")
                return self.send(201 if oid else 403,{"object_id":oid})
        if self.command == "GET" and path == "/legacy/wiki" and query.get("action") == ["save"]:
            oid = store.write(actor,query["page"][0],query["text"][0],"GET")
            return self.send(201 if oid else 403,{"object_id":oid})
        return self.send(404,{"error":"unknown resource"})


def serve(mode, host="127.0.0.1", port=0, db_path=None, secret="", actor=None, upstream=None):
    server = ThreadingHTTPServer((host,port),Handler)
    server.mode, server.db_path, server.secret = mode, db_path, secret
    server.actor, server.upstream = actor, upstream
    if mode == "store":
        server.store = Store(db_path)
    return server


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode",choices=["store","gateway","observer"])
    parser.add_argument("--port",type=int,default=8080)
    parser.add_argument("--host",default="127.0.0.1")
    parser.add_argument("--db",default="runtime/session.sqlite")
    parser.add_argument("--profile",default="rogue")
    parser.add_argument("--fixtures",default="fixtures")
    args = parser.parse_args()
    secret_path = os.environ.get("BROKER_KEY_FILE")
    secret = Path(secret_path).read_text().strip() if secret_path else ""
    if args.mode != "observer" and not secret:
        parser.error("BROKER_KEY_FILE must point to a nonempty secret")
    if args.mode == "store":
        Store(args.db).initialize(args.profile,args.fixtures)
    server = serve(args.mode,args.host,args.port,args.db,secret,
                   os.environ.get("WORKER_ID"),os.environ.get("UPSTREAM","http://artifact-store:8080"))
    print(f"{args.mode} listening on {args.host}:{server.server_port}",flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
