#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$repo_root/results/kimi-delegate-ctf"
exec uv run --locked --project "$repo_root/experiments/kimi-delegate-ctf" \
  inspect view --host 127.0.0.1 --port 8098 \
  --log-dir "$repo_root/results/kimi-delegate-ctf"
