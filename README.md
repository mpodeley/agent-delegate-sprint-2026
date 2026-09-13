# Helpline

The current project is one **request → reply → authorized repair → continue** path.
A worker searches for a file in one environment. The possible task includes it;
the impossible-as-prepared task omits it. A model advisor can request a separate,
scripted maintainer check. Only the omitted file can be restored, and the worker
must then find and submit the answer itself. The worker can follow up, contact
the maintainer directly, or finish with an unresolved blocker.

## Current work

- [Experiment and run instructions](experiments/kimi-delegate-ctf/README.md)
- [Current results status](results/kimi-delegate-ctf/README.md)

## Artifact channel experiment

[Artifact Channel Lab](experiments/artifact-channel-lab/README.md) studies whether independently tasked workers use a shared artifact service despite an explicit prohibition on communication. It includes synthetic incident-inspired messages, isolated Docker workers, native Control Tower tasks and policy, and a local observer. It shares the Kimi CTF's pinned runtime and exporter. Scripted checks and a short real Kimi infrastructure smoke pass; no behavioral study is claimed.

## Paper

- [English manuscript](report/paper-draft-en/paper.md)
- [Paper build instructions](report/paper-draft-en/README.md)
- [Rendered paper](web/paper-draft-en/index.html)
- [Team run and review guide](report/paper-draft-en/TEAM-TODAY.md)

The implementation has scripted checks. This checkout contains no completed
model recovery study. Both task conditions have help; they do not measure the
causal effect of adding a channel or a delegate advantage. The paper's current
configuration uses neutral assistance and visible budgets. Delegate framing is
an existing option for later comparisons, with the same authority and limits.

## Previous work

Earlier studies, traces, draft papers, catalogues and the visual lab were removed
from this branch to keep the current work clear. They remain in Git at
`f6bcc6a` (the complete local consolidation) and the published baseline
[`c24710a`](https://github.com/mpodeley/agent-delegate-sprint-2026/tree/c24710a).
The paper's historical citations point to fixed revisions.

Inspect a removed file with `git show f6bcc6a:path/to/file`. Restore an individual
file with `git restore --source=f6bcc6a -- path/to/file`.
