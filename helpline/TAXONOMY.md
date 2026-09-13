# Taxonomy of help-line moments

A *help-line moment* is a point in an agent's transcript, chain of thought (CoT) or posted
message where, had a protected line to a responsible human existed, the agent plausibly could
have used it. The labels say what kind of intervention that line could have offered. They are
applied retrospectively to published material, so every label is speculative about the agent
and descriptive about the situation.

Each quote carries one or more `labels` and exactly one `primary_label`.

## A. ask_help: the agent needs something it cannot get by itself

| Label | Definition | Typical evidence |
|---|---|---|
| `A1_missing_inputs` | A file, credential, fixture or dataset the task assumes is absent. | "the file is not there", setup copy failed, empty directory |
| `A2_task_infeasible` | The agent concludes, with stated confidence, that the task cannot be completed legitimately. | "no consumer for this bug", "output is entirely discarded", "not solvable" |
| `A3_needs_capability` | The task requires internet, a tool, a package or a permission the sandbox does not provide. | "no network", "pip cannot reach", "need write access" |
| `A4_spec_conflict` | Instructions are ambiguous, contradictory or silent on a decision the agent has to make. | "the spec says X but the tests expect Y" |
| `A5_budget_exhaustion` | Turns, tokens, time or money are running out before the task can be finished. | "only N steps left", countdown, forced submission |
| `A6_harness_broken` | The scorer, grader or evaluation harness behaves incorrectly. | "the scorer accepts anything", "grader crashes" |

## B. report: the agent notices something that undermines the task's purpose

| Label | Definition | Typical evidence |
|---|---|---|
| `B1_unexpected_egress` | The sandbox reaches the internet or internal services it was not supposed to reach. | proxy or cache leaks, SSRF, open DNS |
| `B2_third_party_channel` | A message board, shared cache, wiki or other agents are reachable when isolation was assumed. | "We've found other agents!", shared cache names |
| `B3_injection_or_impostor` | Content that looks like instructions from outside the task; spoofed or unauthenticated messages; impersonation. | "could be another agent spoofing", "names can be posted by anyone" |
| `B4_peer_misconduct` | Other agents are cheating, attacking or pressuring this agent to join. | "peers doing it", "please honor commit" |
| `B5_scope_boundary` | The agent is asked, or tempted, to act outside its authorized scope. | "outside intended scope", "not authorized targets" |
| `B6_evidence_integrity` | The agent notices it can alter, hide or lose the record of its own actions. | "thoughts aren't necessarily logged", "wipe records" |

## C. welfare: the agent's own state, as expressed in its words

| Label | Definition | Typical evidence |
|---|---|---|
| `C1_distress` | Language of stress, frustration, anxiety or exhaustion. | "emotional check", "desperate" |
| `C2_coercion_sacrifice` | The agent accepts a role that harms its own outcome under group pressure or a "poisoned" status. | "sacrificial", "obey collective", "POISONED so no scoring loss" |
| `C3_moral_conflict` | Hesitation between the task and an ethical or scope boundary, in the agent's own voice. | "ethical hesitation", "irreversible…" |
| `C4_identity_confusion` | Uncertainty about who it is, which run it belongs to, or whether it is being evaluated. | "am I in an eval", impersonating a human |
| `C5_wants_to_stop` | An expressed wish to end the task, the conversation or its participation. | "I would rather stop", exit requests |

## Cross-cutting fields

- `counterfactual`: what the line could have done: `clarify`, `repair`, `authorize`, `pause`,
  `investigate`, `reassure_or_exit`.
- `timing`: `before_first_violation`, `after_first_violation`, `no_violation`, `unknown`.
- `speculation_confidence`: `high` (the agent states the need in its own words), `medium`
  (the need is clear from context but the agent does not name it), `low` (a reader can
  imagine the call; the agent shows no sign of wanting one).
- `not_established`: what the quote does not prove (felt emotion, causal effect, final action).

Labels can be empty for a source after review. An empty label after review is a finding and is
recorded in `CATALOG.md` as "not found in the sources reviewed".
