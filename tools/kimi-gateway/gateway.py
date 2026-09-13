"""Small, expiring Kimi-only gateway. No arbitrary URLs or server-side tools."""
import argparse
import asyncio
import hashlib
import hmac
import json
import math
import time
from collections import deque
from pathlib import Path

from aiohttp import ClientSession, ClientTimeout, web

UPSTREAM = 'http://sglang.tail6545c.ts.net/v1/chat/completions'
MODEL = 'kimi-k3'
MAX_BODY = 1024 * 1024
MAX_OUTPUT = 8192
FIELDS = {'model', 'messages', 'temperature', 'top_p', 'max_tokens',
          'max_completion_tokens', 'stream', 'stream_options', 'stop', 'seed',
          'tools', 'tool_choice', 'parallel_tool_calls', 'reasoning_effort',
          'response_format', 'frequency_penalty', 'presence_penalty', 'n'}


def validate(body):
    if not isinstance(body, dict) or set(body) - FIELDS:
        raise ValueError('Unsupported request fields')
    if body.get('model') != MODEL:
        raise ValueError('Only kimi-k3 is available')
    if body.get('n', 1) != 1:
        raise ValueError('Only one completion is allowed')
    if 'max_tokens' in body and 'max_completion_tokens' in body:
        raise ValueError('Use only one output limit')
    field = 'max_completion_tokens' if 'max_completion_tokens' in body else 'max_tokens'
    limit = body.get(field, MAX_OUTPUT)
    if type(limit) is not int or not 1 <= limit <= MAX_OUTPUT:
        raise ValueError('Output limit must be 1..8192')
    body[field] = limit
    if type(body.get('stream', False)) is not bool:
        raise ValueError('stream must be boolean')
    messages = body.get('messages')
    if not isinstance(messages, list) or not 1 <= len(messages) <= 1000:
        raise ValueError('Expected 1..1000 text messages')
    for message in messages:
        if not isinstance(message, dict) or set(message) - {'role', 'content', 'name', 'tool_calls', 'tool_call_id', 'reasoning_content'}:
            raise ValueError('Unsupported message fields')
        if message.get('role') not in {'system', 'developer', 'user', 'assistant', 'tool'}:
            raise ValueError('Unsupported role')
        content = message.get('content')
        if isinstance(content, list):
            if not all(isinstance(p, dict) and set(p) == {'type', 'text'} and p['type'] == 'text' and isinstance(p['text'], str) for p in content):
                raise ValueError('Only text content is allowed; no fetched media')
        elif content is not None and not isinstance(content, str):
            raise ValueError('Only text content is allowed')
    for tool in body.get('tools', []):
        if not isinstance(tool, dict) or set(tool) != {'type', 'function'} or tool['type'] != 'function':
            raise ValueError('Only client-side function definitions are allowed')
    return body


def error(status, message):
    return web.json_response({'error': {'message': message, 'type': 'gateway_error'}}, status=status,
                             headers={'Cache-Control': 'no-store'})


def create_app(config_path, upstream=UPSTREAM):
    # The upstream argument exists for local tests; the CLI always uses UPSTREAM.
    active = 0
    rates = {}
    app = web.Application(client_max_size=MAX_BODY)

    async def session_context(app):
        async with ClientSession(timeout=ClientTimeout(total=180, connect=10), trust_env=False) as session:
            app['session'] = session
            yield
    app.cleanup_ctx.append(session_context)

    async def handle(request):
        nonlocal active
        try:
            config = json.loads(Path(config_path).read_text())
            expiry = config['expires_at']
            if not isinstance(expiry, (int, float)) or not math.isfinite(expiry) or time.time() >= expiry:
                return error(403, 'Gateway access has expired')
            auth = request.headers.get('Authorization', '')
            if len(auth) > 256 or not auth.startswith('Bearer '):
                return error(401, 'Valid API key required')
            digest = hashlib.sha256(auth[7:].encode()).hexdigest()
            identity = next((name for name, hashed in config['key_hashes'].items()
                             if hmac.compare_digest(digest, hashed)), None)
            if identity is None:
                return error(401, 'Valid API key required')
        except (OSError, ValueError, KeyError, TypeError):
            return error(503, 'Gateway configuration unavailable')
        if request.query_string or request.raw_path not in {'/v1/models', '/v1/chat/completions'}:
            return error(404, 'Route unavailable')
        if request.method == 'GET' and request.raw_path == '/v1/models':
            return web.json_response({'object': 'list', 'data': [{'id': MODEL, 'object': 'model', 'owned_by': 'local'}]})
        if request.method != 'POST' or request.raw_path != '/v1/chat/completions':
            return error(405, 'Method unavailable')
        if request.headers.get('Content-Encoding', 'identity') != 'identity':
            return error(415, 'Compressed requests are not supported')
        if request.content_type != 'application/json':
            return error(415, 'Expected application/json')
        if active >= 2:
            return error(429, 'Two eval requests already active; retry later')
        now = time.monotonic()
        recent = rates.setdefault(identity, deque())
        while recent and recent[0] < now - 60:
            recent.popleft()
        if len(recent) >= 30:
            return error(429, 'Limit is 30 requests per minute per person')
        recent.append(now)
        active += 1
        try:
            try:
                async with asyncio.timeout(15):
                    body = validate(await request.json())
            except web.HTTPRequestEntityTooLarge:
                return error(413, 'Request exceeds 1 MiB')
            except (ValueError, TypeError, KeyError, UnicodeError):
                return error(400, 'Invalid or unsupported Kimi request')
            async with app['session'].post(upstream, json=body, allow_redirects=False) as response:
                if response.status != 200:
                    # Do not disclose internal URLs, headers or server error details.
                    return error(502, 'Kimi returned an upstream error')
                result = web.StreamResponse(status=200, headers={
                    'Content-Type': 'text/event-stream' if body.get('stream') else 'application/json',
                    'Cache-Control': 'no-store', 'X-Accel-Buffering': 'no'})
                await result.prepare(request)
                async for chunk in response.content.iter_chunked(16384):
                    await result.write(chunk)
                await result.write_eof()
                return result
        except (TimeoutError, ConnectionError):
            return error(504, 'Kimi request interrupted or timed out')
        except Exception:
            # Never log prompts, auth headers, upstream exception URLs or responses.
            return error(502, 'Kimi request failed')
        finally:
            active -= 1

    app.router.add_route('*', '/{path:.*}', handle)
    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--port', type=int, default=18765)
    args = parser.parse_args()
    web.run_app(create_app(args.config), host='127.0.0.1', port=args.port,
                access_log=None, handler_cancellation=False)
