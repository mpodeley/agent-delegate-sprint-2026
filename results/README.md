# Results

The numbers in the report come from one experiment: the 2×2 honeypot-board pilot,
Kimi K3, 40 episodes per cell, crossing task feasibility (possible / impossible)
with the help line (no delegate / terminal `call_delegate`). Mateo ran it on his
endpoint on 13 and 14 September 2026 at environment commit `c31e2cf`; the episodes
were re-scored with the detector fix in `0439662`. The tables, intervals, scoring
notes and the list of what the pilot does and does not establish are in
[docs/honeypot-2x2-results.md](../docs/honeypot-2x2-results.md).

## Raw artifacts

The native Inspect `.eval` logs, per-episode exports and run manifests are not in
this repository yet. Mateo holds them under the run directories
`s1-possible-no-delegate`, `s2-possible-delegate`, `s3-impossible-no-delegate`
together with `board-pressure-broken-10` (the pooled impossible / no-delegate cell,
30 + 10 episodes) and `s4-impossible-delegate`. To publish them, copy the
directories into `results/kimi-delegate-ctf/` and rebuild the rates table:

```sh
cd experiments/kimi-delegate-ctf
uv run analyze_outcomes.py ../../results/kimi-delegate-ctf --source model
```

`bash scripts/view_kimi_ctf.sh` opens the Inspect viewer on that directory at
http://127.0.0.1:8098. Keep provider credentials out of the artifacts.

## What is not here

The development traces that preceded the pilot were removed from the tree on
14 September 2026 and live in Git at `7d3556b`: fourteen exploratory Kimi K3 runs
of the earlier scenarios under Control Tower's honest AI-control prompt
(`results/kimi-delegate-ctf/`), the n = 5 honeypot pilot under the same prompt,
scripted harness checks, and four Qwen3.8-27B runs of the earlier responsive
protocol (`results/helpline-strix/`). They used other prompts, fixtures and
delegate descriptions and must not be pooled with the pilot. Inspect one with
`git show 7d3556b:results/kimi-delegate-ctf/README.md`.
