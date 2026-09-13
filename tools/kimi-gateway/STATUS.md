# Validation and activation status

2026-09-12: Seven local mock integration tests passed. A real localhost check
returned 401 without a key, 200 for the authenticated Kimi-only model list, 400
for a DeepSeek request, and 200 for one Kimi completion capped at 16 output tokens.
No full eval was run. Both key files and the config are ignored by Git, with
private filesystem permissions. The gateway uses no Krea credential.

Public activation was attempted with:

```sh
tailscale funnel --bg --https=8443 http://127.0.0.1:18765
```

Tailscale returned: “Funnel is not enabled on your tailnet. Contact your administrator.”
A subsequent status check returned “No serve config”. Nothing is publicly exposed.
The local gateway was stopped afterward. An administrator must enable Funnel for
this device before public activation can proceed. No alternate tunnel was created.

The initially generated keys expire 2026-09-13 at 18:59:41 Argentina time.
No keys have been sent to other people. See README.md for start/stop and revocation.
