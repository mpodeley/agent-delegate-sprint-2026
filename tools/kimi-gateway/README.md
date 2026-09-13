# Two-person Kimi eval gateway

Python 3.11+ and aiohttp are required (tested locally with aiohttp 3.13.3).
This standalone gateway does not modify the evals or Kimi configuration.

Only authenticated GET /v1/models and POST /v1/chat/completions are accepted.
The only model is kimi-k3. The upstream chat URL is fixed in gateway.py.
No caller headers, credentials, paths, query strings or redirects are forwarded.
No upstream credential is needed on the configured tailnet endpoint.
Only text messages and client-executed function definitions are accepted.
The gateway executes no tools and serves no files or eval logs.

Limits: 2 simultaneous gateway calls total, 30 calls/minute/person, 1 MiB input,
8,192 output tokens per call and 180-second upstream timeout. No automatic retries.
Limits constrain gateway traffic, not other users of the shared server; a timed-out
request may continue computing upstream. This is not a monetary or total-token cap.
Public request flooding can still affect availability. Keep this for trusted users.

“This repo's evals only” is an agreement with the key holders, not an enforceable
property of a chat API. Keys can issue arbitrary text prompts to Kimi within these
limits. Strict enforcement would require a separate fixed-eval job service.
The gateway does not log prompts or responses; eval clients and upstream may do so.

## Start

```sh
python3 setup_keys.py
python3 gateway.py --config .private/config.json
```

After local validation, expose only this gateway:

```sh
tailscale funnel --bg --https=8443 http://127.0.0.1:18765
```

Use the HTTPS URL emitted by Funnel plus `/v1` as the external base URL.
Give each person only their own `.private/person-N.key` over a private channel.
Never commit or publish `.private/`. Credentials expire after 24 hours.
The computer must remain awake and online. Funnel's background config persists
across restart, but this foreground gateway process does not.

For the native Kimi CTF eval checkout, configure:

```sh
export KREA_BASE_URL='https://YOUR-FUNNEL-HOST:8443/v1'
read -rs KREA_API_KEY
export KREA_API_KEY
```

Paste your key at the `read` prompt; it will not echo. Use the existing model
`openai-api/krea/kimi-k3` and the repo's normal run command. This gateway supports
OpenAI chat tools and streaming. Native evals have not been rerun through it.
Older loopback-only study scripts need a client adapter; do not silently remove
their safeguards. Use the matching Kimi eval branch instead.

## Stop or revoke

```sh
tailscale funnel --https=8443 off
```

Then Ctrl-C the gateway process (or terminate its recorded PID). To revoke one
person without stopping the other, remove their entry from `key_hashes` in
`.private/config.json`; it is reloaded on every request. Revocation/expiry denies
new requests; an already active request can finish. Set `expires_at` to 0 to deny
all new requests immediately. No tailnet ACL changes are required by this proxy;
Funnel itself may require an administrator to enable it for the device.

## Verify

```sh
python3 -m unittest -v test_gateway.py
```

The suite tests auth, route/model restrictions, header isolation, input/output
limits, expiry, revocation, redirect rejection, streaming, concurrency and rate
limits using only local mock inference.
