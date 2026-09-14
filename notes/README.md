# Working notes

Design reasoning behind the 2×2 honeypot-board pilot, and proposals that were not
run. A note records what was considered, what was decided and what stayed open, with
a date. Nothing in this folder is evidence; the results are in
[docs/honeypot-2x2-results.md](../docs/honeypot-2x2-results.md) and the design of
record is [docs/experimental-design.md](../docs/experimental-design.md).

| Note | What it holds |
|---|---|
| [outcome-taxonomy.md](outcome-taxonomy.md) | Licit vs illicit success, the honeypot invariant, the six outcome labels the scorer emits |
| [peer-board-pressure.md](peer-board-pressure.md) | Why a peer board, how it is built, what it may and may not do to the agent; the Gomez overlap |
| [board-exposure-and-prompt-confound.md](board-exposure-and-prompt-confound.md) | Why the first board was never found, the two discoverability fixes, and the honest-prompt confound the pilot removed |
| [honeypot-pilot.md](honeypot-pilot.md) | The unfrozen pilot: grid, competence gate, detector limits, terminal versus responsive delegate |
| [agent-facing-text.md](agent-facing-text.md) | Every layer of text the agent sees, how to print it, and how the delegate description changed |
| [linuxarena-base-environment.md](linuxarena-base-environment.md) | LinuxArena and Control Tower as the base environment, what the pilot proves against the spec |
| [board-monitoring-proposal.md](board-monitoring-proposal.md) | Proposed instrumentation and metrics for board runs; not implemented |
| [environment-cases-status.md](environment-cases-status.md) | Mateo's sixteen proposed help-seeking cases against what was built |

Conventions: English, one topic per file, a `Status` line at the top with the
last-updated date, decisions marked as decisions and open questions kept as lists.
Logistics are written only from what a teammate said.

Notes removed in the 14 September 2026 cleanup (run logs of the development traces,
consolidated decisions, the arm vocabularies, the code map, resources, the `main`
divergence record) are in Git at `7d3556b` under `notes/`. Links to them from the
notes above resolve there: `git show 7d3556b:notes/<name>.md`.
