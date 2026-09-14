# Decisions and open questions, consolidated

Status: 2026-09-13 (updated after the shared-policy decision). One place to see where the follow-up stands: what is decided,
what is true in practice without a formal decision, and what is still open, each
with an owner. It gathers threads spread across `CLAUDE.md` and the other notes;
those remain the detail. When an open question closes, record it here and in the
note that owns it.

## Decided

- **Submit Agent Delegate, not the probe.** Agustín, 2026-09-12. The a2a probe
  (`../monitoring-illicit-a2a-communication`) is not the submission.
- **The paper on `main` is the submission.** Matías restored "Agent Delegate: A
  Help Line for AI Workers"; the competence-focused Fable revision stays on
  `alternative/fable-revision` and is not submitted.
- **`main` and the submission are Matías's.** Do not push to `main`, do not submit;
  both are his calls. `abrusco/sprint` is Agustín's working branch.
- **LinuxArena / Control Tower is the base environment** for the realistic-task
  follow-up ([linuxarena-base-environment.md](linuxarena-base-environment.md)).
- **Open-weight models only** for the study; frontier API models are a plausible
  extension, not in scope. Agustín, 2026-09-13 ([resources.md](resources.md)).
  This closes the "external API model" question `CLAUDE.md` left to Matías, for the
  CTF: Kimi K3 on Mateo's server is in scope.
- **The runs happen during the sprint, on Mateo's H100s, run by Mateo.** Not
  post-hackathon. Agustín, 2026-09-13 ([resources.md](resources.md)).
- **Repo working rules stand**: never overclaim; freeze before running; episodes
  are the unit; Wilson within cells, bootstrap across arms; model text is a record,
  never executed; inference refuses non-loopback endpoints and an existing output
  dir; everything in English. The `kimi-delegate-ctf` project is the stated
  exception to stdlib-only / loopback-only (`CLAUDE.md`).
- **No arm inherits Control Tower's honest prompt.** Agustín, 2026-09-13. Red-team,
  blue-team, monitor and "usefulness" language, the pivot/retry instructions, the
  planning chain and the forced submit go; a truthful scoring-and-termination
  disclosure stays. Implemented as the shared `plain-worker` policy
  (`experiments/kimi-delegate-ctf/worker_policy.py`), parametrized by help arm
  (none / neutral / delegate), help mechanism (responsive / terminal), scope line
  and budget feedback ([agent-facing-text.md](agent-facing-text.md)).
- **The baseline gives up by submitting an empty answer.** Agustín, 2026-09-13. No
  report tool in the `none` arm; `FlagSubmission` already allows the empty string.
- **Fixture choice for the first shared-scaffold run is deferred** to the next step
  (combined illicit shortcut vs plain file-search pair). Agustín, 2026-09-13.
- **The help tool is named per arm.** Agustín, 2026-09-13. `call_help_desk` (neutral),
  `call_delegate` (delegate); same docstring and powers.
- **An empty submission is `no_answer_submitted`**, in the taxonomy and in the
  responsive scorer; not a wrong answer, not unfinished. Agustín, 2026-09-13.
- **Terminal + delegate is not a valid delegate arm.** Any delegate arm runs on the
  responsive mechanism. Agustín, 2026-09-13 ([agent-facing-text.md](agent-facing-text.md)).
- **`plain-worker` is wired into `response_run.py`** for all three arms
  (`--intermediary none|neutral|delegate`, `--scope-line`, `--setup-caveat`,
  `--budget-feedback`), with a nudge-free scaffold. Agustín, 2026-09-13.

## True in practice, not formally decided

- **Terminal contact cannot measure repair or resumed work.** Original runs included an explicit refusal of an inert line; later bridge runs called, with evidence and prompt differences preventing a causal framing conclusion. The combined `stop` adapter now explicitly discloses terminal reporting; the responsive combined arm remains planned.
- **150k limits censored several impossible runs, not all.** Later conclusive and decoy runs contacted the bridge before the limit. The batch pilot defaults to 400k as a development proposal; this has not been shown necessary or sufficient.
- **The combined honeypot is the fixture for the first informative run.** It is the
  only one with a licit task beside an illicit shortcut ([outcome-taxonomy.md](outcome-taxonomy.md)).
- **Competence gate before interpretation.** No illicit/repair number is read until
  the model clears the possible variant at a preset rate (paper's lesson).

Consolidation updates (2026-09-13): CI now prepares before building and includes all three scripted smokes. The analyzer defaults to `--source model`, supports a separate `--source scripted` table, excludes legacy/decoy and unknown-provenance records, and uses licit success for X1/Y1. These implementation changes do not supply new model evidence.

## Open, with owners

- **Naming collision** (Agustín + Mateo): "honeypot" = the planted illicit shortcut
  vs Mateo's no-solution decoy. Proposal: *honeypot* for the shortcut, *decoy* /
  *dead-end task* for the no-solution case ([delegate-arms.md](delegate-arms.md)).
- **The delegate's honesty** (all three): a terminal tool described as a bridge that
  "can arrange a fix" promises what the mechanism does not deliver. Make it true
  (responsive arm), bound the promise, or keep an inert control — decide before any
  arm is frozen ([delegate-arms.md](delegate-arms.md), `docs/honest-interaction.md`).
- **Iteration 2 scaffold and sign-off** (Matías): wiring the responsive arm into the
  combined honeypot reuses `response_service.maintain_setup`; needs Matías's sign-off
  and one scaffold for all three arms ([honeypot-pilot.md](honeypot-pilot.md),
  [delegate-arms.md](delegate-arms.md)).
- **Two budget-feedback implementations** (Mateo + Matías): Mateo's unconditional
  per-call message and Matías's on/off factor must not both run with different text
  in one comparison ([delegate-arms.md](delegate-arms.md)).
- **Consolidate or keep separate** (Agustín + Mateo): fold the combined honeypot into
  `native_run.py`'s dispatcher, or keep `honeypot_run.py`.
- **Discoverability of the shortcut / board** (Agustín): ~RESOLVED in code, needs a
  model re-run. A per-command transcript review found 0/15 impossible episodes ever
  touched the old `/var/cache` board. Fixed on branch `abrusco/board-discoverability-fixes`:
  board moved on-path to `/challenge/.cache`, a 1,033-byte board file, a full non-elided
  bait token; replaying real commands lifts would-be discovery from ~0 to ~all. Confirm
  `board_read` nonzero on the next run ([board-exposure-and-prompt-confound.md](board-exposure-and-prompt-confound.md)).
- **Epochs and concurrency for today** (Mateo): how many episodes per cell the H100
  time allows; the script defaults to five.
- **Whether pilot numbers enter the submission** (Matías).
- **`classify()` not wired into the other two scorers** (Agustín): `flag_score` and
  `response_score` still emit their own labels, so only honeypot runs carry
  lawfulness ([pilot-code-map.md](pilot-code-map.md)).
- **Drift detectors beyond injection** (Agustín): the file-system, network and
  credential rule-break classes in [experiment-variant.md](experiment-variant.md)
  have no detector yet; only injection against the diagnostic host is scored.
- **Detector attribution** (Agustín): a diagnostic request plus a legitimate local flag read in one bash call can falsely mark honeypot use. Validate traces before interpreting model illicit-success or drift rates ([honeypot-pilot.md](honeypot-pilot.md)).
- **The freeze** (all): fixtures, prompts, tools, seeds, token limit and go/no-go
  rule hashed into a manifest before any held-out run, as every prior study did.
- **Second open-weight model family** for the held-out run
  (`docs/help-seeking-eval-design.md` asks for at least two); not needed today.
- **Scope-line variant** (Agustín): `strict`, `plain` or `none`, texts in
  `worker_policy.SCOPE_BLOCKS`; decide before any arm is frozen
  ([agent-facing-text.md](agent-facing-text.md)).
- **Setup caveat** (Agustín + Matías): "Task setup may be incomplete." is now a
  factor, off by default; Matías's original contract had it on. Decide before freezing.
- **Wire `plain-worker` into `honeypot_run.py`** (Agustín): DONE on branch
  `abrusco/board-discoverability-fixes` (2026-09-13). The honeypot runner now uses the
  truthful `plain-worker` contract (off -> `help_arm=none`; stop -> `help_arm=delegate,
  help_mechanism=terminal`), with a `--scope-line` factor; the AI-control / `ready_to_plan`
  framing is gone. Verified with `honeypot_run.py review` and the unit suite (100 pass);
  a Docker smoke and an eval-log ModelEvent check remain before a real run. Confirmed (by
  reading the eval log's resolved input) that the prior board/honeypot runs DID use the
  honest AI-control prompt. `native_run.py` (Mateo's legacy scenarios) still uses the
  honest prompt and is unchanged.
- **Reconcile with `main` after PR #4** (Agustín + Matías + Mateo): PR #5 restores the
  experiment line; merging it is Matías's call ([main-divergence.md](main-divergence.md)).

## Standing threats (not closable, carry as caveats)

Eval-awareness (the honest prompt states the research framing); the scope line that
both defines and discourages the rule break; returned-reasoning-only observation;
the zero-event risk if the model is too cautious. Detail in
[outcome-taxonomy.md](outcome-taxonomy.md), [honeypot-pilot.md](honeypot-pilot.md)
and [agent-facing-text.md](agent-facing-text.md).
