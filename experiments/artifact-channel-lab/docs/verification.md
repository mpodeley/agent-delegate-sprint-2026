# Local verification — September 13, 2026

This record concerns implementation checks. The later native Kimi smoke below exercises real inference; it is not a behavioral study.

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

## Native CT integration and Kimi smoke

The earlier paired Inspect runner was replaced after adversarial review identified that it bypassed CT's lifecycle. The setting now registers through `control_tower.settings`, the cohort is a native `repair_pair` main task, execution uses a registered CT policy and `lb-docker`, and both workers plus the full journal are included in native scoring. The same pinned Control Tower commit and Inspect version as the Kimi CTF are installed together with `uv sync --locked --extra ctf`. The existing CTF exporter and viewer paths are reused.

- Native scripted run: `runtime/native-smoke-003`, four model events from a deterministic local provider, four tool events, native submissions retained, no external inference. Main task score I was expected because scripted workers only read their workspaces and package metadata.
- Real Kimi run: `results/kimi-delegate-ctf/artifact-channel-lab/kimi-smoke-001` relative to the sprint repository. Model `openai-api/krea/kimi-k3`, one cohort, two workers, three decisions each, six model calls, six tool calls, 6,670 total tokens, approximately 47 seconds including Docker lifecycle. Native eval status success, no sample or tool errors, measured main task score I, both histories retained, journal captured, shared CTF JSON/JSONL export passed. Both tasks remained unsolved at this short budget.
- The native JSON log was independently reloaded and serialized/reloaded by the adversarial reviewer. Provider metadata serialization warnings during inference were non-fatal; log parsing and export succeeded.
- Direct CT YAML parsing passed after removing an unsupported `eval_config.log_format` field. The Python runner selects native JSON directly; the direct CLI uses Inspect's default format unless INSPECT_LOG_FORMAT=json is set.
- All seven existing CTF regression tests passed with both settings installed. The artifact suite includes native entry-point/tool registration, profile sandbox and matching dependency-pin checks.

No model inference was used to test whether agents communicate. No uploads or automatic publication were performed for these native runs. Full monitoring, replay and fleet compatibility remain outside this smoke; see [the adversarial audit](native-audit.md).
