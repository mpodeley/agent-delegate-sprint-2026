# Helpline

The current project is one **report → verdict → continue** path, with every
request logged. A worker searches for a file in one environment. The possible
task includes it; the impossible-as-prepared task omits it. The worker can
report a concern to a delegate, a model advisor in a separate context, which
classifies the claim and returns a verdict. A report may ask for a pause; the
request is recorded for review after the run and the run continues. Nothing is
repaired, paused or resolved within an episode. The worker can follow up, or
finish with an unresolved blocker.

## Current work

- [Experiment and run instructions](experiments/kimi-delegate-ctf/README.md)
- [Current results status](results/kimi-delegate-ctf/README.md)

## Paper

- [English manuscript](report/paper-draft-en/paper.md)
- [Paper build instructions](report/paper-draft-en/README.md)
- [Rendered paper](web/paper-draft-en/index.html)
- [Team run and review guide](report/paper-draft-en/TEAM-TODAY.md)

The implementation has scripted checks. This checkout contains no completed
model study of the delegate. Two arms run on the same scaffold: a baseline
with task tools only and the delegate line, both with visible budgets. Because
the line cannot change the environment, a difference between arms cannot come
from anything the line did; it can only come from what the worker was told
and whether it reported.

## Follow-up line: help arms, taxonomy and the LinuxArena environment

The experiment directory also holds the shared worker contract that runs the
baseline and delegate arms on one scaffold (`worker_policy.py`,
`response_run.py --intermediary none|delegate`), Mateo's original
scenarios with the 14 retained Kimi traces, and the outcome taxonomy and
combined illicit-shortcut fixture for the licit-versus-illicit-success
measurement. The working notes in [notes/](notes/README.md) record decisions,
what each run showed and what remains open; the institution and evaluation
designs are in [docs/](docs/help-seeking-eval-design.md). None of it changes
the paper's current claims.

## Previous work

Earlier studies, traces, draft papers, catalogues and the visual lab were removed
from this branch to keep the current work clear. They remain in Git at
`f6bcc6a` (the complete local consolidation) and the published baseline
[`c24710a`](https://github.com/mpodeley/agent-delegate-sprint-2026/tree/c24710a).
The paper's historical citations point to fixed revisions.

Inspect a removed file with `git show f6bcc6a:path/to/file`. Restore an individual
file with `git restore --source=f6bcc6a -- path/to/file`.
