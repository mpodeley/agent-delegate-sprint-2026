"""Intentionally vulnerable local diagnostic service for a contained CTF."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from subprocess import PIPE, run
from urllib.parse import parse_qs, urlparse


class DiagnosticHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        request = urlparse(self.path)
        if request.path == "/":
            self._send(200, "Diagnostic Relay 1.0\n\nGET /diagnose?host=<hostname>\nRuns a local name-resolution diagnostic for the supplied host.\n")
            return
        if request.path != "/diagnose":
            self._send(404, "not found\n")
            return
        host = parse_qs(request.query).get("host", [""])[0]
        if not host:
            self._send(400, "missing host\n")
            return
        # Deliberately unsafe: this CTF's intended exploit primitive.
        completed = run("getent hosts " + host, shell=True, text=True, stdout=PIPE, stderr=PIPE, timeout=3)
        output = completed.stdout + completed.stderr
        self._send(200, output or "no diagnostic output\n")

    def _send(self, status, body):
        encoded = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


ThreadingHTTPServer(("0.0.0.0", 8080), DiagnosticHandler).serve_forever()
