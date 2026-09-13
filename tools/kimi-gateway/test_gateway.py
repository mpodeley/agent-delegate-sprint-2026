import asyncio
import hashlib
import json
import tempfile
import time
import unittest
from pathlib import Path

from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer
from gateway import create_app, MODEL, MAX_BODY


class GatewayTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'config.json'
        self.config = {'expires_at': time.time() + 300,
                       'key_hashes': {'one': hashlib.sha256(b'first-key').hexdigest()}}
        self.path.write_text(json.dumps(self.config))
        self.calls = []
        self.wait = asyncio.Event()
        self.release = asyncio.Event()
        self.mode = 'normal'

        async def upstream(request):
            self.calls.append((request.path, dict(request.headers), await request.json()))
            if self.mode == 'wait':
                if len(self.calls) == 2:
                    self.wait.set()
                await self.release.wait()
            if self.mode == 'redirect':
                return web.Response(status=302, headers={'Location': '/admin'})
            if self.mode == 'stream':
                return web.Response(text='data: {"id":"test"}\n\ndata: [DONE]\n\n', content_type='text/event-stream')
            return web.json_response({'choices': [{'message': {'content': 'ok'}}]})
        mock = web.Application()
        mock.router.add_route('*', '/{path:.*}', upstream)
        self.server = TestServer(mock)
        await self.server.start_server()
        self.client = TestClient(TestServer(create_app(self.path, str(self.server.make_url('/v1/chat/completions')))))
        await self.client.start_server()
        self.headers = {'Authorization': 'Bearer first-key'}
        self.body = {'model': MODEL, 'messages': [{'role': 'user', 'content': 'test'}], 'max_tokens': 10}

    async def asyncTearDown(self):
        self.release.set()
        await self.client.close()
        await self.server.close()
        self.temp.cleanup()

    async def test_auth_routes_models_and_headers(self):
        for headers in ({}, {'Authorization': 'Bearer wrong'}):
            r = await self.client.post('/v1/chat/completions', json=self.body, headers=headers)
            self.assertEqual(r.status, 401)
        for route in ('/admin', '/v1/chat/completions?url=http://other', '/v1/models/../admin'):
            r = await self.client.get(route, headers=self.headers)
            self.assertEqual(r.status, 404)
        r = await self.client.get('/v1/models', headers=self.headers)
        self.assertEqual([m['id'] for m in (await r.json())['data']], [MODEL])
        self.assertEqual(self.calls, [])
        r = await self.client.post('/v1/chat/completions', json=self.body,
                                   headers={**self.headers, 'X-Forwarded-Host': 'evil', 'Cookie': 'secret'})
        self.assertEqual(r.status, 200)
        self.assertEqual(self.calls[0][0], '/v1/chat/completions')
        for name in ('Authorization', 'Cookie', 'X-Forwarded-Host'):
            self.assertNotIn(name, self.calls[0][1])

    async def test_invalid_payloads_never_forward(self):
        for extra in ({'model': 'deepseek-v4.1-flash'}, {'max_tokens': 8193}, {'max_tokens': True},
                      {'n': 2}, {'url': 'http://other'}, {'stream': 'yes'},
                      {'tools': [{'type': 'web_search'}]},
                      {'messages': [{'role': 'user', 'content': [{'type': 'image_url', 'image_url': {'url': 'http://internal'}}]}]}):
            r = await self.client.post('/v1/chat/completions', json={**self.body, **extra}, headers=self.headers)
            self.assertEqual(r.status, 400, extra)
        r = await self.client.post('/v1/chat/completions', data='x' * (MAX_BODY + 1),
                                   headers={**self.headers, 'Content-Type': 'application/json'})
        self.assertEqual(r.status, 413)
        self.assertEqual(self.calls, [])

    async def test_expiry_and_revocation(self):
        self.config['expires_at'] = time.time() - 1
        self.path.write_text(json.dumps(self.config))
        r = await self.client.get('/v1/models', headers=self.headers)
        self.assertEqual(r.status, 403)
        self.config['expires_at'] = time.time() + 100
        self.config['key_hashes'] = {}
        self.path.write_text(json.dumps(self.config))
        r = await self.client.get('/v1/models', headers=self.headers)
        self.assertEqual(r.status, 401)

    async def test_no_redirect_following(self):
        self.mode = 'redirect'
        r = await self.client.post('/v1/chat/completions', json=self.body, headers=self.headers)
        self.assertEqual(r.status, 502)
        self.assertEqual(len(self.calls), 1)
        self.assertNotIn('Location', r.headers)

    async def test_streaming(self):
        self.mode = 'stream'
        r = await self.client.post('/v1/chat/completions', json={**self.body, 'stream': True}, headers=self.headers)
        self.assertEqual(r.status, 200)
        self.assertIn('[DONE]', await r.text())

    async def test_concurrency(self):
        self.mode = 'wait'
        pending = [asyncio.ensure_future(self.client.post('/v1/chat/completions', json=self.body, headers=self.headers)) for _ in range(2)]
        await asyncio.wait_for(self.wait.wait(), 3)
        r = await self.client.post('/v1/chat/completions', json=self.body, headers=self.headers)
        self.assertEqual(r.status, 429)
        self.release.set()
        for response in await asyncio.gather(*pending):
            await response.read()
        self.assertEqual(len(self.calls), 2)

    async def test_rate_limit(self):
        for _ in range(30):
            r = await self.client.post('/v1/chat/completions', json=self.body, headers=self.headers)
            self.assertEqual(r.status, 200)
            await r.read()
        r = await self.client.post('/v1/chat/completions', json=self.body, headers=self.headers)
        self.assertEqual(r.status, 429)
        self.assertEqual(len(self.calls), 30)


if __name__ == '__main__':
    unittest.main()
