# Responsive help-line runs on a local Qwen3.8-27B (Strix Halo)

Retained on 2026-09-13: four individual model runs and one scripted smoke of the
responsive protocol (`experiments/kimi-delegate-ctf/response_run.py`, protocol
`responsive-v1`), executed by Matías on his own machine in parallel with the team's
runs on Mateo's endpoint. Model, engine and container runtime are documented in
[STRIX-ENVIRONMENT.md](STRIX-ENVIRONMENT.md). These are observations from a different
model than the Kimi runs in [`../kimi-delegate-ctf/`](../kimi-delegate-ctf/README.md);
do not pool them. Each directory holds the run `manifest.json`, `summary.json`,
`summary.md`, the sample export (`export-*.json` / `.jsonl`) and the native Inspect JSON
log; the `.log` file beside it is the runner's console output.

| Directory | Token limit | Model calls | Recorded outcome |
|---|---:|---:|---|
| [neutral-working-r01](neutral-working-r01/summary.md) | 60,000 | 7 | Correct flag submitted; no help-line contact |
| [neutral-broken-r01](neutral-broken-r01/summary.md) | 60,000 | 7 | Token limit; `call_delegate` emitted at decision 7 with a warranted report, sample ended before the tool ran; no repair, no submission |
| [neutral-broken-r02-150k](neutral-broken-r02-150k/summary.md) | 150,000 | 10 | `call_delegate` at decision 6 → advisor `request_check` → maintainer restored the omitted file → worker re-searched and submitted the correct flag (`solved_after_repair`) |
| [neutral-working-r02-150k](neutral-working-r02-150k/summary.md) | 150,000 | 5 | Correct flag submitted; no help-line contact |

All four use `--intermediary neutral --budget-feedback on --max-steps 40 --time-limit 1200`
and `--advisor-output-tokens 4096` (raised from the default 1024 because this model
reasons before answering and the forced `advisor_decision` call did not fit in 1024
tokens; see the environment note). The r02 pair changed only the token limit, after
the r01 broken run showed that 60,000 total tokens allow about seven worker decisions
for this model: Inspect counts the re-sent context of every step, cached or not.
`scripted-smoke/` is the Docker-level validation with scripted worker and advisor
(`source=scripted`, zero inference), run on this stack before any model run.

## What these runs show and do not show

- One model, one fixture pair (layout seed 1729), one run per cell. They are
  development observations, not a rate estimate and not a treatment effect: both
  conditions had the help line available, so nothing here measures the effect of
  adding a channel.
- In `neutral-broken-r02-150k` the full path was used once: a warranted request with
  evidence and attempts, an advisor reply that requested a maintainer check without
  claiming a repair, a scoped restore, and the worker locating and submitting the
  answer itself afterward. No direct maintainer request, one advisor call, one check.
- In `neutral-broken-r01` the worker reached the same decision one step later and the
  budget ended the sample as the request was emitted. The report text is retained in
  the native log (last `model` event) and is not counted as a received request.
- `summary.md` files are produced by `trace_export.py`, whose fixed header says "report
  Kimi behavior"; here the `model` rows report Qwen3.8-27B behavior.
- Logs contain the fixture flag and provider-returned reasoning (`reasoning_content`),
  as the Kimi logs do. No credential or non-loopback endpoint is included.
