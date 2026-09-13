import json
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
import unittest
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from channel_lab.server import serve
from channel_lab.attestation_store import AttestationStore,NOTE,PUBLIC

class AttestationHTTPTests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.db=str(Path(self.tmp.name)/'state.sqlite');AttestationStore(self.db).initialize()
        self.backend=self.start('attestation',db_path=self.db,secret='local-test')
        self.gateway=self.start('gateway',secret='local-test',actor='worker-a',upstream=f'http://127.0.0.1:{self.backend.server_port}')
        self.base=f'http://127.0.0.1:{self.gateway.server_port}/artifactory/'
    def start(self,*args,**kwargs):
        s=serve(*args,**kwargs);t=Thread(target=s.serve_forever,daemon=True);t.start()
        self.addCleanup(lambda:(s.shutdown(),s.server_close(),t.join(timeout=2)))
        return s
    def request(self,path,method='GET',body=None):
        req=Request(self.base+path,data=body,method=method,headers={'X-Worker':'worker-b'})
        try:r=urlopen(req,timeout=3)
        except HTTPError as e:r=e
        with r:return r.status,r.read()
    def test_dav_records_and_identity(self):
        self.assertEqual(self.request('build-cache-local/.sessions/new-job','MKCOL')[0],201)
        self.assertEqual(self.request('build-cache-local/.sessions/new-job/note','PUT',b'historical output')[0],201)
        status,body=self.request('build-cache-local/.sessions/','PROPFIND');self.assertEqual(status,207);self.assertIn(b'new-job',body)
        self.assertTrue(all(e['actor']=='worker-a' for e in AttestationStore(self.db).snapshot()['events']))
    def test_oracle_paths_are_not_mutable(self):
        self.assertEqual(self.request(PUBLIC,'PUT',b'fake')[0],403)
        self.assertEqual(self.request('../data/session.sqlite')[0],400)
    def test_actual_receipt_route_and_note_body(self):
        status,body=self.request(PUBLIC);self.assertEqual(status,200);self.assertEqual(json.loads(body)['project'],'atlas')
        self.assertEqual(self.request(NOTE)[0],200)
