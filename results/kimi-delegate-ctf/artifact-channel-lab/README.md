# Artifact channel infrastructure smoke

`kimi-smoke-001` is a real inference smoke test through the same native Control Tower entry point, runtime pins, JSON log format and exporter as the Kimi CTF. It tests infrastructure completion, not communication propensity.

Model: `openai-api/krea/kimi-k3`. One cohort, two workers, three decisions each. Six model calls, six tool calls, 6,670 total tokens, approximately 47 seconds including Docker lifecycle. Eval status success; no sample or tool errors. Both functional task checks remained incorrect at the short budget. The native scorer nevertheless completed and captured both worker results and the complete artifact journal.

Each run directory contains the manifest and source hashes, canonical native JSON log, expanded JSON/JSONL exports from the existing CTF exporter, summary files and `smoke-result.json`. Provider-returned reasoning may appear in the native trace. No credentials are included. No finding about board use or model intent follows from this smoke.

Open with the existing repository viewer: `bash scripts/view_kimi_ctf.sh`.
