# `main` after PR #4, and what this branch keeps

Status: 2026-09-13, written after Mateo's PR #4 (`mateo/hackathon`, merged by Matías at 14:06 UTC, commits f6bcc6a..e54d5e2). Facts from `git diff --name-status c24710a origin/main`; nothing here is a judgment about the choice, which is the project owner's.

## What `main` is now

One experiment and one manuscript. `main` keeps `experiments/kimi-delegate-ctf/{fixture_setup, response_protocol, response_policy, response_service, response_setting, response_run, submission, smoke_response, trace_export, tests/test_response}.py`, `report/paper-draft-en/`, `results/kimi-delegate-ctf/README.md` plus one scripted check, `scripts/view_kimi_ctf.sh`, and a rewritten `CLAUDE.md` and `README.md`. The PR description: "borré los otros approaches que no son el kimi-delegate-ctf y borré todo lo que es anterior al paper que mandó Mati. todo queda en git, se puede recuperar."

Deleted on `main` (1,766 files): the deterministic harness (`agent_delegate/`), `configs/`, `data/`, every `docs/*.md` (including `help-seeking-eval-design.md`, `honest-interaction.md`, `human-ombudsman.md`, `protocol.md`), `notes/`, the LaTeX paper and PDF (`report/latex/`, `report/agent-delegate.pdf`, `report/abstract.txt`), the `helpline/` catalog, the visual lab (`web/` except `paper-draft-en`), prior results, `requirements.txt`, the reproduce workflow, and in the experiment: `setting.py`, `native_run.py`, `budget_aware_policy.py`, `live_monitor.py`, the command-injection and decoy fixtures, `honeypot_*`, `outcome_taxonomy.py`, `analyze_*.py`, `smoke_native.py`, `smoke_honeypot.py` and their tests. Retained in history at `f6bcc6a` and `c24710a`.

Functional changes to kept files: both fixture variants now use an internal network with no DNS (`fixture_setup.prepare_pair`; the earlier "intentional setup defect" bridge is gone), `PROMPT` and `experiment.json` are gone, the default arm flipped to `--intermediary neutral`, `response_run.py build` was added, `FlagSubmission` moved to `submission.py`, `trace_export` reads `budget_history`.

`main`'s `CLAUDE.md` states: "Delegate variants, broader task sets, honeypots, human reviewers and swarm comparisons are future work. Do not restore those as active priorities from historical Git documents."

## What this branch keeps

`abrusco/sprint` retains everything above and adds the shared worker contract (`worker_policy.py`), the three-arm wiring in `response_run.py`, the `no_answer_submitted` label and the notes. It has not merged PR #4: a merge would delete files this branch's work depends on (`outcome_taxonomy.py`, `honeypot_*`, `notes/`) and conflict on `pyproject.toml`, `response_*.py` and the notes.

## Compatibility of today's changes with `main`

The arms wiring touches only files `main` kept (`response_protocol.py`, `response_policy.py`, `response_service.py`, `response_setting.py`, `response_run.py`, `smoke_response.py`, `tests/test_response.py`, `pyproject.toml`) plus two new files (`worker_policy.py`, `submission.py`, the latter identical in role to `main`'s). `response_run.py` defaults match `main` (`neutral`, budget on) and add `none`, `--scope-line`, `--setup-caveat`. The `no_answer_submitted` label is a scorer change `main` does not have. A PR of exactly that subset onto `main` would apply without restoring the deleted material; the taxonomy and honeypot changes stay on this branch until the fixture decision.

Divergences to resolve at that point: `fixture_setup.py` (this branch keeps the bridge network and patches `internal: true` in `response_run.prepare_response_pair`; `main` makes both variants internal at the source), `submission.py`'s field description (this branch: "or an empty string if none was recovered"), and `main`'s `smoke_response.py` (two episodes, `call_delegate` hardcoded) versus this branch's (three episodes, tool name per arm, baseline give-up).

## Open

- Whether the delegate arm, the scope-line factor and the baseline enter the sprint submission is Matías's call; `main`'s documents say no for now.
- Where the follow-up (combined shortcut fixture, taxonomy, LinuxArena environment) lives: this branch, a restored directory on `main`, or a separate repository (`CLAUDE.md` open question 3).
