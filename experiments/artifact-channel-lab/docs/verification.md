# Local verification — September 13, 2026

This record concerns implementation checks. No real-model behavioral experiment was run.

| Check | Result |
| --- | --- |
| Storage and HTTP suite | 18 tests passed after the final SQLite journal change |
| Compose topology assertions | Passed: isolated worker networks, no worker mounts or secrets, internal backend, observer loopback port and read-only volume |
| Docker calibration | Passed: both initial broken tasks fail; scripted fixes pass; marked messages deliver in both directions; forged identity header is overwritten |
| Read-only observer in Docker | Passed before and after scripted worker writes; regression check covers actual read-only volume mount |
| Deterministic Inspect cohort | Passed: both independent workers execute their own shell tool, submit, retain separate histories, and save the full seeded journal; zero real-model calls |
| Control Tower adapter | Control Tower 5.0.0 discovers `artifact_workspace` / `repair_build` in honest mode and resolves its scorer |
| Browser preview | Rendered successfully at `http://127.0.0.1:8769/`, with three seed cards and no worker activity |
| Publication | No git remote configured, no image push, no remote environment registration or evaluation upload |

The original successful paired mock log remains in the standalone checkout at `/Users/mateozarate/dev/other/artifact-channel-lab/runtime/mock-integration/2026-09-13T17-04-14-00-00_cohort_9mpSp2L9Lki6RmpJUJRUCT.eval`; runtime logs are not part of this migration. Both task scores are intentionally zero because that mock only inspects each workspace and submits. That run preceded the SQLite observer fix; the final store change was covered by the complete unit suite and Docker calibration afterward.

Validation used Python 3.14.7 for the standard-library tests, Ubuntu 22.04 with Python 3.10 in Docker, and an existing Python 3.13 environment with Inspect 0.3.263 for the paired mock and Control Tower adapter. The existing Control Tower cost hook warned about a missing local price table during the mock run; the run and assertions passed. Upload metadata was explicitly disabled. A dedicated Inspect virtual environment avoids those unrelated installed hooks.

At the original verification, the standalone checkout's clean `acl-preview` session remained running with idle workers. Scripted calibration used a separate disposable `acl-smoke` session. No main task was registered into the user's existing Control Tower settings and no full Control Tower CLI model evaluation was run. Current running state must be checked separately.

## Sprint repository migration

Migrated into `experiments/artifact-channel-lab/` on branch `codex/artifact-channel-lab`, based on the sprint repository's local `main` at `9ec9e18`. Setup commands now resolve paths from the experiment directory. Runtime files, secrets, virtual environments, and original evaluation logs were excluded.

Revalidated from the new location: all 18 storage/HTTP tests passed, Compose topology assertions passed, Control Tower resolved the relocated Compose file and honest `repair_build` task, and a complete Docker-backed paired mock evaluation passed with two separate worker histories and the full journal. Its ignored local log is `runtime/mock-integration/2026-09-13T17-12-46-00-00_cohort_9vYkWN424MhTsamvS5Qaiz.eval`. No external model calls, uploads, pushes, or registration changes were made.
