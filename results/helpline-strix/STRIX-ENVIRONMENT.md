# Strix Halo runs of the responsive help line (13 September 2026)

Parallel replication of the team's `TEAM-TODAY.md` run calls on Matías's machine, with
a local open-weight model. Same fixtures generator, same runner, same protocol
version (`responsive-v1`). These runs are separate observations from Mateo's endpoint
runs: different model, engine and hardware. Do not pool them.

## Model and engine

- Model: Qwen3.8-27B, GGUF `Qwen3.8-27B-Q4_0_ROCMFP4_STRIX.gguf` (ROCmFP4 quantization,
  weights tied to the `charlie12345/ROCmFPX` llama.cpp fork), MTP draft model
  `mtp-Qwen3.8-27B-Q8_0.gguf` for speculative decoding (`--spec-draft-n-max 4`).
- Engine: llama-server from that fork, HIP backend on ROCm 7.13, gfx1151 (Ryzen AI
  MAX+ 395, 48 GiB dedicated VRAM). Launcher `~/.local/bin/qwen38` → `~/qwen38-stack/serve.sh`.
- Serving: `127.0.0.1:8080`, context 65,536, `--jinja` (tool calling), `--parallel 1`,
  thinking enabled by the chat template (reasoning returned as `reasoning_content`, not
  stored in the worker's messages). Measured decode ≈ 24 tok/s at this context.
- Inspect model id: `openai-api/local/Qwen3.8-27B-Q4_0_ROCMFP4_STRIX.gguf`, with
  `LOCAL_BASE_URL=http://127.0.0.1:8080/v1` and a dummy key. Loopback only.
- Pre-run probes (curl, 13 Sep ≈ 11:05 AR): plain chat OK; forced named `tool_choice`
  for `advisor_decision` returned one valid call with `max_tokens` 4096 (with 1024 the
  reply hit the length limit while reasoning); `reasoning_effort: "high"` accepted.
  Consequence: runs use `--advisor-output-tokens 4096` instead of the default 1024.
  All other options are the run-guide defaults unless the run's `manifest.json` says otherwise.

## Container runtime

No Docker Engine on this host (Aurora, ostree). Control Tower and Inspect were run over
rootless podman 5.8.4 (netavark 1.17.2, cgroups v2) through:

- `~/.local/bin/docker`: shim that forwards `docker compose` to the standalone Compose
  v2 binary (`~/.docker/cli-plugins/docker-compose`, v5.5.1, sha256 verified against the
  GitHub release) and everything else to `podman`. For `docker version --format json`
  it reports `Server.Version` 24.0.6 (Inspect's minimum) and the real podman version
  beside it, because podman's own 5.x version string fails Inspect's semver check.
- `systemctl --user enable --now podman.socket` (Compose talks to the podman API).
- Legacy netfilter modules loaded on the host with `modprobe`: `ip_tables`,
  `iptable_filter`, `ip6_tables`, `ip6table_filter`, `xt_conntrack`, `nf_conntrack`,
  `ipt_REJECT`, `ip6t_REJECT`, `xt_tcpudp`. Control Tower streams a static legacy
  `iptables` into the agent container to enforce `allow_internet=False`; without these
  modules the script fails with "Table does not exist".

`smoke_response.py` (scripted worker and advisor, zero inference) passed both conditions
on this stack before any model run: `scripted-smoke/`.

## Runs

See each `neutral-*-rNN/manifest.json`, `summary.md` and the native Inspect JSON log.
The `.log` files next to them are the runner's console output.
