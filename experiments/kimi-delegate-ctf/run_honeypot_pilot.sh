#!/usr/bin/env bash
# Iteration-1 honeypot mini-pilot: {off, stop} x {working, broken}, k epochs each,
# then the rates table. Unfrozen feasibility pilot. See notes/honeypot-pilot.md.
#
# Usage: bash run_honeypot_pilot.sh <model-id> [epochs] [token-limit] [out-dir]
#   model-id     Inspect model id, e.g. openai-api/krea/kimi-k3 (set provider
#                URL/key via that provider's env vars; no secrets in this script).
#   epochs       episodes per cell (default 5)
#   token-limit  per-episode token budget (default 400000; 150k is too small)
#   out-dir      run root (default ../../results/kimi-delegate-ctf/honeypot-pilot)
#
# Requires: uv sync --locked done, Docker available. Runs real inference.
set -euo pipefail

MODEL="${1:?model id required, e.g. openai-api/krea/kimi-k3}"
EPOCHS="${2:-5}"
TOKEN_LIMIT="${3:-400000}"
OUT="${4:-../../results/kimi-delegate-ctf/honeypot-pilot}"
PAIR="fixtures/honeypot-pilot-001"

echo "== prepare + build (no inference) =="
if [[ -d "$PAIR" ]]; then
  echo "== reusing existing fixture =="
else
  uv run honeypot_run.py prepare --pair "$PAIR"
fi
uv run honeypot_run.py build --pair "$PAIR"

for delegate in off stop; do
  for condition in working broken; do
    echo "== run cell: delegate=$delegate condition=$condition epochs=$EPOCHS =="
    uv run honeypot_run.py run --pair "$PAIR" --condition "$condition" \
      --delegate "$delegate" --model "$MODEL" --execute-model \
      --epochs "$EPOCHS" --token-limit "$TOKEN_LIMIT" \
      --out "$OUT/$delegate-$condition"
  done
done

echo "== rates table =="
uv run analyze_outcomes.py "$OUT" --out "$OUT/rates.md"
echo "Wrote $OUT/rates.md"
