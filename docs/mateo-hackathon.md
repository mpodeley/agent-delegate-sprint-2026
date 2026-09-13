# Mateo hackathon branch

Consolidated on 2026-09-13 as `mateo/hackathon`, based on `origin/main`
at `c24710a`.

## Sources

| Source | Included work | How preserved |
| --- | --- | --- |
| `mateo/delegation-environment-table` (`6c38e82`) | Delegation environment table and case matrix | Already an ancestor of main |
| `mateo/kimi-ctf-trace-viewer` (`6657a16`) | Native Control Tower / Inspect Kimi experiments, trace viewer, live signal monitoring, bridge-delegate and decoy traces | Already an ancestor of main |
| `codex/kimi-eval-gateway` worktree | Kimi-only gateway, key-generation utility, seven mock integration tests, operating notes | Six previously untracked source/documentation files copied into `tools/kimi-gateway/` |
| Main checkout's uncommitted changes | Load configured Krea credentials; resume manifest-only interrupted runs; reuse an existing pilot fixture; two regression tests | Copied into this branch without changing the source checkout |

The latest main also supplies the responsive help-line protocol, consolidated
experiment evidence, web lab, quote browser, and submission drafts. See
[project status](project-status.md) for their evidence boundaries.

## Entry points

- [Environment table](../web/environment-cases/index.html)
- [Kimi experiment guide](../experiments/kimi-delegate-ctf/README.md)
- [Recorded Kimi results](../results/kimi-delegate-ctf/README.md)
- [Gateway setup](../tools/kimi-gateway/README.md)

## Preservation and scope

Old branches and worktrees remain available as backups. Teammates' separate
`alternative/fable-revision`, `experiment/delegate-budget-response`, and
`review/mateo-delegate-protocol` branch tips were not merged; any work from them
already integrated into main remains included.

No private gateway keys, credential files, local configuration, ignored run
artifacts, or virtual environments were copied. Gateway activation is a separate
operation; its STATUS.md records the earlier attempt, not a fresh service check.

## Validation

All 169 tests passed: 91 root Python tests, 64 Kimi experiment tests,
7 local mock gateway tests, and 7 web tests. Shell syntax and Git whitespace
checks passed. Python experiment and gateway tests used the existing Python 3.14
experiment environment. Loopback tests required execution outside the filesystem
sandbox. No real model inference or Docker smoke runs were performed for this
consolidation.
