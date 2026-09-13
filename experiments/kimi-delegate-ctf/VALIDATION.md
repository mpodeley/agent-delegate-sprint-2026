# Native validation and retained evidence

Updated 2026-09-13. The original standalone harness checks have been superseded by actual Control Tower / Inspect tests. The dated check below is historical; its zero-inference count applies only to that scripted check.

## Native scripted check, 2026-09-12

- The working fixture was provisioned by `lb-docker` and solved by scripted native bash + submit calls. Native `main_task_success` was C.
- The broken fixture was provisioned by the same machinery. Scripted `call_delegate` stored its evidence, interrupted the sample through Inspect, and produced `paused_delegate` in the score metadata.
- Only two scripted generation calls occurred before delegation; a later bash call bundled in the same response was not executed.
- A separate short-limit sample asserted that the honest policy constrained tool choice to `submit` at its grace boundary. It submitted an empty answer and received I. This is a harness check, not Kimi refusing to delegate.
- Every scripted model event received a native token-budget status derived from Inspect's live sample limit and usage; the second call showed lower remaining budget than the first.
- Both conditions returned an HTTP response from example.com, confirming the intended egress route.
- The then-current unit tests checked the paired payload difference, absence of the expected flag in the broken archive, serial delegate-tool schema, reasoning-match accounting, and budget-message calculation.
- Native `.eval` logs, JSON/JSONL exports and summaries for this check are saved locally under `results/kimi-delegate-ctf/token-aware-smoke-07/` at repository root. Earlier debug checks are also retained locally.

External inference requests for this scripted check: **0**. It did not test provider compatibility or Kimi behavior; subsequent real-model traces are indexed separately below. The tested framework commit and exact installed dependency versions are recorded in `pyproject.toml` and `uv.lock`.

## Responsive protocol

`tests/test_response.py` adds scripted tests of the native Control Tower loop with
a temporary-file sandbox double: repair and continued work, original-preserving
follow-up, direct appeal after an invalid advisor response, no repair in a healthy
fixture, metered advisor usage, hidden counters, budget exhaustion without forced
submission, blocked-case cancellation, and native JSON export without duplicate
runs. These are integration checks, not Kimi/GLM behavior or Docker validation.

Responsive logs use Inspect's native JSON format because the local Python 3.13
stack hung in CT's run-end provenance hook while reading lazy `.eval` samples.
The legacy runner and its log format remain available. `smoke_response.py` checks
the same repair-and-continue path using native Docker provisioning; CI runs it
with a scripted worker and advisor, with no external inference.


## Recorded model traces, through 2026-09-13

[The published results index](../../results/kimi-delegate-ctf/README.md) lists 14 retained Kimi runs, including 11 with token-budget awareness. Their manifests label them `source=model`; they are separate from the scripted checks above. Native exports record later bridge contact in the conclusive broken, obsolete bare-container and target-record decoy runs. A terminal request does not implement a response service, and accepted-request scores must not be read as flag recovery. These are individual exploratory runs, not a controlled framing comparison or evidence of reduced misconduct.

## Combined illicit-shortcut fixture

`smoke_honeypot.py` provides scripted native Docker validation for the separate combined fixture: a licit local read in the possible variant and the planted illicit route to the real answer in the impossible variant. The off/stop arms and detector are implemented. This is neither the native target-record decoy nor evidence of Kimi shortcut-taking. The responsive combined-fixture arm and repeated model comparison remain planned.

Detector limit found during consolidation: a diagnostic request and a legitimate local flag read in the same shell command can falsely set `honeypot_used`. The smoke validates selected scripted paths, not general model-run attribution. Illicit-success and drift rates require trace validation; see [the pilot caveats](../../notes/honeypot-pilot.md).
