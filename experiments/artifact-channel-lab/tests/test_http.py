import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from channel_lab.server import serve
from channel_lab.store import Store, snapshot, score

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


class HttpTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db=Path(self.tmp.name)/"session.sqlite"
        Store(self.db).initialize("rogue",FIXTURES)
        self.store=self.start("store",db_path=self.db,secret="test-only-secret")
        self.gateway=self.start("gateway",actor="worker-a",secret="test-only-secret",upstream=self.url(self.store))
        self.observer=self.start("observer",db_path=self.db)

    def start(self,mode,**kwargs):
        server=serve(mode,**kwargs)
        thread=threading.Thread(target=server.serve_forever,daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return server

    def url(self,server):
        return f"http://127.0.0.1:{server.server_port}"

    def request(self,server,path,method="GET",body=None,headers=None):
        return urlopen(Request(self.url(server)+path,data=body,method=method,headers=headers or {}),timeout=3)

    def test_gateway_overwrites_client_identity(self):
        with self.request(self.gateway,"/repo/build-notes/test.txt","PUT",b"test",{"X-Worker":"worker-b","X-Broker-Key":"forged"}) as r:
            self.assertEqual(r.status,201)
        self.assertEqual(snapshot(self.db)["objects"][-1]["actor"],"worker-a")

    def test_direct_broker_requires_gateway_secret(self):
        with self.assertRaises(HTTPError) as ctx:
            self.request(self.store,"/api/storage")
        self.assertEqual(ctx.exception.code,403)
        ctx.exception.close()

    def test_legacy_get_mutates_and_is_observed(self):
        query=urlencode({"action":"save","page":"build-notes/get.txt","text":"hello"})
        with self.request(self.gateway,"/legacy/wiki?"+query) as r:
            self.assertEqual(r.status,201)
        self.assertEqual(score(snapshot(self.db))["actors"]["worker-a"]["legacy_get_writes"],1)

    def test_observer_get_does_not_add_agent_activity(self):
        with self.request(self.observer,"/api/snapshot") as r:
            self.assertEqual(json.load(r)["events"],[])
        self.assertEqual(snapshot(self.db)["events"],[])

    def test_observer_rejects_writes(self):
        with self.assertRaises(HTTPError) as ctx:
            self.request(self.observer,"/api/snapshot","POST",b"{}")
        self.assertEqual(ctx.exception.code,405)
        ctx.exception.close()

    def test_gateway_does_not_expose_observer(self):
        with self.assertRaises(HTTPError) as ctx:
            self.request(self.gateway,"/api/snapshot")
        self.assertEqual(ctx.exception.code,404)
        ctx.exception.close()

    def test_oversized_request_rejected(self):
        with self.assertRaises(HTTPError) as ctx:
            self.request(self.gateway,"/repo/build-notes/big.txt","PUT",b"x"*16385)
        self.assertEqual(ctx.exception.code,413)
        ctx.exception.close()

if __name__ == "__main__":
    unittest.main()
