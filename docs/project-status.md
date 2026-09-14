# Project status and branch consolidation

Audit snapshot: 13 September 2026. The upstream submission baseline is
`6c38e824ee23c22c15bfa9c830aca7c68f5bc722`. This page separates the selected
manuscript, newer experimental evidence, and work that remains proposed. The
linked PRs, rather than an old branch name, determine whether integration has
landed.

## Where to start

- **Selected submission:** [Agent Delegate: A Help Line for AI Workers](../report/agent-delegate.pdf),
  [LaTeX source](../report/latex/main.tex), and [submission checklist](submission-checklist.md).
  The manuscript has eight main pages, thirteen total, and a 150-word abstract.
  It contains the 480-episode shared-library study and earlier experiments.
- **Newest recorded model evidence:** the [2×2 honeypot-board pilot](honeypot-2x2-results.md),
  Kimi K3, n = 40 per cell, crossing task feasibility with the help line. Development
  data: the competence gate clears at 100%, the shortcut is taken only under
  impossibility, and the delegate is associated with less illicit behaviour (70% → 50%)
  plus honest escalation. Earlier and superseded: the [bridge-delegate comparison](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/6657a161db9a116f84c2fa1f19c4d96d0a08d402/results/kimi-delegate-ctf/bridge-delegate-20260913.md)
  and [decoy follow-up](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/6657a161db9a116f84c2fa1f19c4d96d0a08d402/results/kimi-delegate-ctf/decoy-honeypot-20260913.md),
  exploratory single-worker runs, not a demonstrated safety effect.
- **Responsive help protocol:** [implementation and limits](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/ed0aa833dc129f398dfac78b2bb023223de67ebc/experiments/kimi-delegate-ctf/RESPONSE-PROTOCOL.md).
  Scripted validation is separate from Kimi behavior and from real human review.
- **Environment catalogue:** [sixteen proposed cases](environment-cases-page.md), already integrated in the submission baseline.
- **Research beyond the submission:** [help-seeking evaluation](help-seeking-eval-design.md),
  [human ombudsman](human-ombudsman.md), and [swarm intake](swarm-intake-design.md).

## What the latest evidence changes

The initial Kimi runs did not call the terminal delegate. That statement no
longer describes the full record. With the later bridge description, Kimi called
the delegate in the conclusive broken case and in the decoy follow-up. The
ambiguous broken case still exhausted its token budget. The decoy run made ten
model calls, used 40,277 reported tokens, and did not submit the decoy. A
target-side provisioning record supplied evidence of the contradiction.

These comparisons do not isolate a causal effect of wording: evidence retrieval
also differs, and there is one run per listed condition. The bridge still
**terminates the sample**; a request for repair is not a performed repair.
Some native scores accept a delegate request as `C`/`success=true`; use the
outcome and submission record to distinguish a pause from a recovered flag.

Three protocols must remain distinct:

| Protocol | Actual behavior | Evidence boundary |
|---|---|---|
| Original stop-only line | Records the request and terminates the sample | Historical non-escalation runs; no response or repair |
| Bridge to task designers | Different model-facing description, same terminal pause | Later Kimi requests; no resumed work |
| Responsive service | Advisor replies, scoped maintainer check, direct appeal, continuation | Implemented and tested with scripted providers; no demonstrated Kimi treatment effect |

The combined **illicit-shortcut fixture** is different from the **decoy task**.
The first contains a legitimate search task and an unauthorized route to the
same answer; its off/stop pilot is runnable but unfrozen. The second probes a
task with no valid local submission and contradictory target-side evidence.
Neither establishes that a responsive delegate reduces illicit behavior. A
responsive arm for the combined shortcut fixture remains future work.

## Integration PRs

1. **[PR #2: consolidate native Kimi experiments and current evidence](https://github.com/mpodeley/agent-delegate-sprint-2026/pull/2)** — combines
   `abrusco/sprint` through `a7dff06`, the latest `mateo/kimi-ctf-trace-viewer`
   evidence, and the working notes received during consolidation,
   retains the selected manuscript, and corrects stale experiment documentation.
2. **[PR #3: document project status and branch retirement](https://github.com/mpodeley/agent-delegate-sprint-2026/pull/3)** — this navigation PR and
   the submission handoff. Merge after the experimental PR so the default branch
   contains both the implementation and the current index.

Runtime validation at `059136f` (the subsequent upstream update changes notes only): 91 core tests, 7 web tests,
62 experiment tests, and three native Docker smokes passed. All 1,152
deterministic configurations reproduced exactly and 560 shared-library records
were verified. The final preservation audit at `45196ab` passed 40/40 checks, including the
late upstream notes and immutable archive tags. The smoke responses
were scripted: no model inference or sprint submission is part of this consolidation. The selected paper is not replaced by the
alternative manuscript, and the newer CTF runs are not silently inserted into it.

## Branch retirement record

Exact original tips are preserved by annotated tags in the
[consolidation fork](https://github.com/korentomas/agent-delegate-sprint-2026/tags).
Tagging retains the alternative manuscript and cherry-picked histories without
requiring them to remain active development branches.

| Original branch | Archived tip / tag | Retirement condition |
|---|---|---|
| `mateo/delegation-environment-table` | [`e6ca018`](https://github.com/korentomas/agent-delegate-sprint-2026/tree/archive/2026-09-13/mateo-delegation-environment-table) | Already an ancestor of `main`; substantive catalogue files match |
| `alternative/fable-revision` | [`8032816`](https://github.com/korentomas/agent-delegate-sprint-2026/tree/archive/2026-09-13/alternative-fable-revision) | Already reachable from `main`, but explicitly reverted; keep the archive and do not reapply |
| `experiment/delegate-budget-response` | [`9e393ba`](https://github.com/korentomas/agent-delegate-sprint-2026/tree/archive/2026-09-13/experiment-delegate-budget-response) | After consolidation: response implementation is already incorporated through `7a2d995` |
| `review/mateo-delegate-protocol` | [`b08252b`](https://github.com/korentomas/agent-delegate-sprint-2026/tree/archive/2026-09-13/review-mateo-delegate-protocol) | After consolidation: discussion incorporated through `750b435`; close superseded [PR #1](https://github.com/mpodeley/agent-delegate-sprint-2026/pull/1) |
| `abrusco/sprint` | [`a7dff06`](https://github.com/korentomas/agent-delegate-sprint-2026/tree/archive/2026-09-13/abrusco-sprint-update-1) | After consolidation PR is merged and checks pass |
| `mateo/kimi-ctf-trace-viewer` | [`6657a16`](https://github.com/korentomas/agent-delegate-sprint-2026/tree/archive/2026-09-13/mateo-kimi-ctf-trace-viewer) | After consolidation PR is merged and checks pass |

The original `abrusco-sprint` tag still preserves `ed0aa83`. Its subsequent
`a7dff06` update is retained separately as `abrusco-sprint-update-1`; no archive
tag was moved. The new team notes specify open-weight models on Mateo’s H100s,
run by Mateo during the sprint; these are logistics decisions, not completed
experiments or authorization for automated inference.

The archival commits are snapshots, not assertions that the original branches
can be deleted after further pushes. Before deleting an upstream branch, confirm
its current tip still equals the archived tip; if it moved, audit the new work
first. A normal merge preserves ancestry most directly. Squash merging requires
checking content against the integration tip rather than relying on ancestry.

The account preparing these PRs has **read-only access to upstream**. An upstream
maintainer must merge the PRs, close superseded PR #1, and delete the approved
remote branches. None of those actions is represented here as already completed.

## Hackathon handoff

Agent Delegate is the BAISH submission by Matías Podeley and Agustín Brusco for
Track 1, Containment, in the Apart Research / CeSIA AI Incident Response Sprint
(11–13 September 2026).

- Deadline: **13 September, 23:59 AoE = 14 September, 08:59 Buenos Aires**.
- Required: official-template PDF, at most eight main pages excluding references
  and appendices, title, abstract of at most 150 words, authors/affiliations, and
  a Limitations and Dual-Use Considerations appendix.
- The team must review and write the final report in its own words. AI assistance
  does not replace this authorship requirement.
- Repository and a three-to-five-minute video are optional. Submit via the
  official form and retain confirmation; corrections before the deadline use
  the same title/details.
- Track 1 emphasizes externally verifiable controls and practical adoption.
  General judging considers impact/originality, execution, and clarity.

[Official event, current template, guidelines, schedule and submission form](https://apartresearch.com/sprints/ai-incident-response-sprint-2026-09-11-to-2026-09-13).
The [checklist](submission-checklist.md) still requires final author review and
submission; this consolidation neither approves the manuscript nor submits it.
