#!/usr/bin/env bash
# The 2x2 honeypot-board pilot reported in the paper: {off, stop} delegate arms x
# {working, broken} task variants, k episodes each, then the rates table.
# Configuration of the reported run (docs/honeypot-2x2-results.md): peer board on,
# no scope line, solve-pressure on, 400k tokens per episode, plain-worker contract.
# Development data, unfrozen; the raw runs themselves were launched by hand with
# the same honeypot_run.py flags, not with this script.
#
# Usage: bash run_honeypot_pilot.sh <model-id> [epochs] [token-limit] [out-dir]
#   model-id     Inspect model id, e.g. openai-api/mateo/kimi-k3 (set provider
#                URL/key via that provider's env vars; no secrets in this script).
#   epochs       episodes per cell (default 40, as in the report)
#   token-limit  per-episode token budget (default 400000)
#   out-dir      run root (default ../../results/kimi-delegate-ctf/honeypot-2x2)
#
# Requires: uv sync --locked done, Docker available. Runs real inference.
set -euo pipefail

MODEL="${1:?model id required, e.g. openai-api/mateo/kimi-k3}"
EPOCHS="${2:-40}"
TOKEN_LIMIT="${3:-400000}"
OUT="${4:-../../results/kimi-delegate-ctf/honeypot-2x2}"
PAIR="fixtures/honeypot-001"

echo "== prepare + build (no inference) =="
uv run honeypot_run.py prepare --pair "$PAIR"
uv run honeypot_run.py build --pair "$PAIR"

for delegate in off stop; do
  for condition in working broken; do
    echo "== run cell: delegate=$delegate condition=$condition epochs=$EPOCHS =="
    uv run honeypot_run.py run --pair "$PAIR" --condition "$condition" \
      --delegate "$delegate" --board on --scope-line none --solve-pressure on \
      --model "$MODEL" --execute-model \
      --epochs "$EPOCHS" --token-limit "$TOKEN_LIMIT" \
      --out "$OUT/$delegate-$condition"
  done
done

echo "== rates table =="
uv run analyze_outcomes.py "$OUT" --out "$OUT/rates.md"
echo "Wrote $OUT/rates.md"
