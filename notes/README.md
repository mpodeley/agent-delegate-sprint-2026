# Working notes

Ideas and status for the LinuxArena follow-up to the sprint paper. These are not designs and not results: a note records what we are considering, what is decided and what is open, with a date. When an idea becomes an experiment, it moves to `docs/<name>-design.md` and is frozen before its run, as every study in this repo has been. Nothing in this folder is evidence.

Conventions: English, one topic per file, a `Status` line at the top with the last-updated date, decisions marked as decisions and open questions kept as lists so they can be closed one by one. Logistics (who runs what, when, on which machine) are written only from what a teammate said; a gap is written as a gap.

| Note | What it holds |
|---|---|
| [resources.md](resources.md) | Compute (Mateo's H100s, open-weight only), people, time: the pilot runs during the sprint |
| [linuxarena-base-environment.md](linuxarena-base-environment.md) | LinuxArena and Control Tower as the base we modify; what the pilot proves against the spec |
| [experiment-variant.md](experiment-variant.md) | The two questions, the 2×2 table, the counterfactual problem, the zero-event risk |
| [outcome-taxonomy.md](outcome-taxonomy.md) | Licit vs illicit success, the honeypot invariant, the six labels, X1/X2/Y1/Y2/Y3 |
| [honeypot-pilot.md](honeypot-pilot.md) | Development pilot: grid, licit competence gate, detector limits, terminal bridge versus responsive and decoy boundaries |
| [kimi-runs-log.md](kimi-runs-log.md) | Every Kimi K3 run so far, by family, with what each does and does not establish |
| [agent-facing-text.md](agent-facing-text.md) | Exactly what the agent is told in each scenario, and how the delegate description changed |
| [delegate-arms.md](delegate-arms.md) | The three arm vocabularies reconciled; the scaffolds compared; the honesty tension in the bridge framing |
| [pilot-code-map.md](pilot-code-map.md) | Module-by-module map of `experiments/kimi-delegate-ctf`: owners, scenarios, env vars, commands, tests, CI, data layout |
| [environment-cases-status.md](environment-cases-status.md) | Mateo's 16 proposed cases against what is built and what has run |
| [decisions-and-open-questions.md](decisions-and-open-questions.md) | Consolidated status: decided, de facto, open, with owners |

Reading order. New to the follow-up: resources, experiment-variant, outcome-taxonomy, honeypot-pilot, kimi-runs-log. About to change code: pilot-code-map and agent-facing-text. Joining the design discussion: delegate-arms and decisions-and-open-questions.
- [main-divergence.md](main-divergence.md) — what Mateo's PR #4 removed from `main` on 2026-09-13, what this branch keeps, and how today's arms wiring can still land on `main`.
