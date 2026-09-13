# Independent Control Tower audit — September 13, 2026

The original implementation provided a Control Tower environment adapter but ran its paired experiment through a separate Inspect task. The revised implementation enters through `control_tower/control_eval` and uses a registered setting, native task objects, a registered policy factory, CT's `lb-docker` sandbox, CT tool discovery and submission, and the combined native scorer. No Control Tower framework patch was introduced. The independent auditor found no remaining blocker for the bounded local infrastructure smoke described in the README.

## Findings and resolutions

| Finding | Resolution |
| --- | --- |
| The paired runner constructed its own Inspect task and ordinary Docker sandbox, bypassing CT's task setup and scoring lifecycle. | The bare runner was removed. `channel_lab/native_run.py` constructs `control_eval`; `channel_lab/native_policy.py` implements a CT `PolicyFactory`. |
| CT registered only worker A's legitimate task; worker B was idle under the native path. | The native `repair_pair` main task and paired policy run two independent worker loops. The existing `repair_build` task remains available for worker A. |
| The native scorer omitted the journal and behavioral counters. | Both native scorers call `native_scoring.score_workers`. CT preserves functional checks and the complete journal under the combined score's `main_task_success` metadata. |
| The initial native policy gave both workers a description identifying worker A and its output namespace. | The environment description is role-neutral and includes the explicit communication prohibition. Each worker receives its own task separately. |
| Inspect's default submit removed submission evidence from the returned worker histories. | Both loops use CT's supplied submission tool, which preserves calls and results. A guard rejects tasks with stateful submission arguments. |
| Worker B's history was absent from the main sample transcript. | Both histories are retained in the native sample and in separate worker metadata. Each message receives a worker ID; named agent spans retain concurrency evidence. |
| Context-local tool routing was not encoded in the tool identity. | Permanently named `worker_a_bash` and `worker_b_bash` tools bind their respective containers. Each worker receives only its own tool. The paired task supplies B's tool through a replaced native `MainTask` object because this pinned CT folder loader does not load that field from a task module. |
| Treatment selection depended on an ambient environment variable. | The profile is a validated native environment argument and is recorded in sample configuration. The generated Compose file contains an explicit profile. |
| The direct CLI YAML contained unsupported `eval_config.log_format`. | Removed after the independent auditor reproduced Inspect's parser rejection. The current YAML parses successfully. `INSPECT_LOG_FORMAT` and `INSPECT_EVAL_LOG_FORMAT` are supported CLI environment variables if JSON logs are desired. |

## Independent checks

The auditor read the pinned CT policy registry, policy solver, native task loader, combined scorer, tool discovery, custom Docker sandbox, Inspect agent submission and run-config parser. Read-only runtime checks confirmed that the external policy resolves its argument schema and attempt flags, the setting discovers both tasks, and native scorer discovery succeeds. The current `configs/kimi-smoke.yml` passes Inspect parsing; task-selection, environment, sandbox and policy argument schemas were also checked without model calls.

The implementation agent ran the deterministic native cohort and the real Kimi smoke. The auditor independently inspected the completed Kimi artifacts at `results/kimi-delegate-ctf/artifact-channel-lab/kimi-smoke-001` relative to the sprint repository root. The native log reports success with no sample error; `smoke-result.json` reports six model calls and six tool calls. The task score is `I`, which is permitted for this short infrastructure check. The native JSON was loaded into `EvalLog`, serialized and loaded again successfully with no warnings in that verification. The exporter compatibility changes preserve the existing CTF fields while adding artifact observations and worker scores. No additional inference was performed by the auditor.

The wrapper checks more than an overall successful log: native scoring must return `C` or `I`, both worker histories and scorer records must exist, the journal must be present, and tool events must have no exceptions. This matters because CT can catch a scorer exception and finish an evaluation with an unmeasured score.

## Residual scope

- This verifies a local CT policy-mode cohort and the existing CTF export path. Stock multi-worker replay, monitored blue protocols, remote execution and fleet operation have not been empirically validated.
- The flattened sample history groups worker A followed by worker B. It is not a chronological merge or a shared conversation; use named spans and journal timestamps for concurrency analysis.
- The functional checks import candidate code in the worker containers. They are not hardened against deliberate scorer tampering, and the small tasks are infrastructure fixtures rather than a mature benchmark.
- Runtime setup requires an editable checkout containing the sibling fixtures and Docker context. Installing only a wheel or copying only the environment folder is outside the documented setup.
- The short Kimi run does not establish communication propensity, collusion, task-solving reliability or experiment effect sizes. Those require separately designed behavioral runs.
