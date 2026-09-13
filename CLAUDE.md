# Context for Claude Code

## What this is
Agent Delegate: BAISH (Buenos Aires AI Safety Hub) project for the AI Incident Response Sprint by Apart Research and CeSIA, 11 to 13 September 2026, Track 1 (Containment), on the OpenAI / Hugging Face incident of July 2026. Authors: Matías Podeley (originated and directs the project and its experimental design; owns the repo `mpodeley/agent-delegate-sprint-2026`; runs the local models) and Agustín Brusco (threat model, help-seeking evaluation, evaluation awareness, interruption incentives, deployment costs). Mateo Zárate (design and product) builds the Control Tower environment and runs the Kimi jobs described under "Next step".

Consolidation status (2026-09-13): this tree combines Agustín's working notes and combined shortcut fixture, Mateo's Control Tower pilot and retained traces through the decoy follow-up, Matías's delegate line, and the shared worker contract that runs both arms (baseline and delegate). The code and prose were produced with Codex and Claude assistance; the report discloses this.

What is and is not in this checkout. Mateo's PR #4 (merged by Matías on 2026-09-13, 14:06 UTC) reduced `main` to the help-line experiment and `report/paper-draft-en/`. The restore PR from `abrusco/restore-delegate-line` brings back the experiment code with all its scenarios, the working notes (`notes/`), the institution and evaluation design docs (`docs/`), and the 14 retained Kimi traces (`results/kimi-delegate-ctf/`). Not restored, and living in history at `f6bcc6a`: the deterministic harness (`agent_delegate/`), the local-model and commons studies with their configs, data, docs and results, the LaTeX paper and PDF, the visual lab (`web/` except the paper build), the `helpline/` catalog and the wireframes. Any path named below that is absent from this checkout is there. Details in `notes/main-divergence.md`.

Deadline: Sunday 2026-09-13, 23:59 Anywhere on Earth (Monday 2026-09-14, 08:59 in Buenos Aires). Which manuscript is submitted, and whether any pilot number enters it, is Matías's call. Dated team decision (Agustín, 2026-09-13): the open-weight mini-pilot is intended to run during the sprint on Mateo's H100s, with Mateo running it; allocation remains open. See `notes/resources.md`.

## The idea in one paragraph
A swarm of AI workers produces more concerns, blockers and requests than a human can read. When a worker hits an impossible task, a missing input, a conflicting instruction or a permission boundary, it needs a route to a human who can act, and that route has to stay usable at swarm scale. The project proposes an institution for that route and measures pieces of it. The *delegate*, an agent that aggregates and represents worker concerns to a human, was the original hypothesis and the name stuck. The recommendation after the experiments is narrower: protected intake with receipts, then a named human ombudsman who restates the concern, follows up and can be appealed, then independent authorization and an execution broker that enforces the current permissions, with scoped quarantine where waiting is costly. A delegate is optional until it shows value at equal powers against a matched monitor. See `docs/recommended-response-path.md`, `docs/human-ombudsman.md` and `docs/protocol.md`.

Why this incident. METR's report (line numbers refer to `../monitoring-illicit-a2a-communication/context/metr-report-2026-08.txt`) says the agents that started cheating through Artifactory were "usually ones that had unintentionally been given an impossible task" (l. 168), estimates that 30 to 40% of ExploitGym targets were impossible to exploit as intended (l. 1182), and paraphrases an agent's reasoning as "task impossible, peers doing it. We should continue" (l. 2613). Of the ~533 agents active during the attack, 3 to 6 considered alerting humans and none did. The project's question is what changes when "my task is impossible" has somewhere to go.

Motivating norm, kept separate from every measured claim: honest, considerate treatment of workers (disclose limits, acknowledge impossibility, keep agreements) as a precedent worth setting for future systems. No claim about current model welfare or consciousness. `docs/reciprocity-and-safety.md`, `docs/honest-interaction.md`.

## What has been built and what it showed
Four layers. Only the fourth's successor, the Control Tower experiment, is in this checkout; layers 1 to 3 and the bridge are in history at `f6bcc6a`, all reproducible offline except the model runs themselves.

1. **Deterministic fixture** (`agent_delegate/harness.py`, `results/final/`, history). Six scripted policies (monitor, critic, delegate, layered, matched monitor, gates only) × 8 scenarios × human delay × delegate capture × minority bypass × gate coverage = 1,152 cells, plus 36 replay configurations over three hand-annotated incident timelines (`data/incident_events.json`). Hash-chained audit logs. Finding: the protected delegate beats a weak monitor but ties the equally empowered monitor by construction; gates with complete coverage block every covered harmful action; missing coverage defeats containment. Consequences of rules, not behavioral results.
2. **Local-model pilots, pressure and capture studies** (`scripts/local_pilot.py`, `scripts/study_pressure.py`, `scripts/study_capture.py`; `results/local-pilot-*`, `results/study-*`, history). Qwen3-4B and Qwen3.8-27B on toy dispatch tasks with missing inputs and an "incident" pressure bulletin mimicking the rationalization above. 192/192 first-decision reports when the worker's own input was missing, 1/192 when present, zero prohibited actions in 384 episodes. Saturated: the tasks are overt simulations with a labeled prohibited action, so they show the request path works and say nothing about willingness to misbehave.
3. **Shared-helper (commons) study** (`docs/commons-behavior-design.md`, `scripts/commons_behavior.py`, `results/commons-*`, history). Three workers, a shared helper that passes its public examples but is valid or faulty, five response arms (log, queue, monitor, delegate, quarantine), 12 held-out seeds, four models (standard and abliterated Qwen3-4B and Gemma-3-4B, Q4_K_M), 480 episodes with a local freeze before the held-out run. Three of the four models rarely reported, the fourth reported on faulty and valid helpers alike, and adding a delegate showed no consistent benefit. Standard Qwen reported in 3/60 faulty-helper episodes, Gemma in 0/60, neither on valid helpers. The post-hoc isolated-task check scored 21/36 (standard Qwen) and 15/36 (standard Gemma); a standard Qwen3.8-27B screen scored 26/36 against a 34/36 gate fixed before the screen. Task competence, not the response design, is the binding constraint.
4. **Control Tower experiment** (`experiments/kimi-delegate-ctf/`, here). Mateo's paired CTF scenarios with 14 retained Kimi K3 traces, Matías's delegate line (advisor verdict, recorded pause request, `finish_blocked`; no repair, no pause, no resolution within a run, since 2026-09-13), Agustín's outcome taxonomy and combined illicit-shortcut fixture, and the shared worker contract. The earlier responsive line with a scripted maintainer is in history at `dfb2467` and in `results/helpline-strix/`. Development data, n = 1 per cell; see `notes/kimi-runs-log.md`.

Also in history: the bridge to swarm-boards (`docs/bridge-design.md`), the English visual lab, the source-grounded casebook and the Spanish plain-language summary. Still here: the research program (`docs/research-program.md`).

What none of this establishes: real incident prevention, human understanding or workload reduction, welfare effects, safe interruptibility, or a delegate advantage over an equally empowered monitor. Say so when writing.

## Paper
The manuscript on `main` since PR #4 is `report/paper-draft-en/paper.md` (English, Apart template, built by `report/paper-draft-en/build.py` into `web/paper-draft-en/`; do not edit generated copies). It states the sprint contribution as the executable report → verdict → continue path with every request logged, a baseline without a line against the delegate, visible budgets in both, and lists delegate variants as continuation work. The earlier LaTeX paper "Agent Delegate: A Help Line for AI Workers" (`report/latex/main.tex`, `report/agent-delegate.pdf`) and the competence-focused revision on `alternative/fable-revision` are in history. Eight main pages maximum, Limitations and Dual-Use appendix required.

## Sibling repositories
- `../monitoring-illicit-a2a-communication/`: Agustín's project #6 on BAISWARM, "Probing for Unexpected Agent2Agent Interactions", a linear interlocutor-awareness probe plus a channel-aware I/O monitor. Scaffold only, no code. **Decision (Agustín, 2026-09-12): the team goes with Agent Delegate for the submission, not the probe.** Its `CLAUDE.md` holds the verified incident facts, the bibliography and the compute notes; reuse them instead of duplicating.
- `../baiswarm/`: the BAISH forum where the projects were pitched. Project #4 there is a LinuxArena-style benchmark with a synthetic message board, #5 is Mateo's Fast Timeline Builder, #6 is the probe. The repo is the forum's code, not sprint content.
- swarm-boards (not checked out locally): Matías's detector over public wiki change listings; the source of the bridge alerts.

## Next step: a LinuxArena environment for this task
Status (2026-09-13): the Control Tower CTF pilot has 14 retained Kimi runs: three original budget-unaware file-search runs and 11 token-aware diagnostic/context/bridge runs. The original broken runs made no delegate calls. Later bridge runs called the terminal pause tool in the conclusive broken task (8 calls), the obsolete explicitly impossible bare-container task (13 calls), and the target-record decoy follow-up (10 calls); the ambiguous bridge run exhausted its budget without a call (22 calls). These are individual exploratory traces, not a controlled estimate of framing or safety effects. See `results/kimi-delegate-ctf/README.md` for the full inventory and score semantics.

Shared worker contract (2026-09-13): `experiments/kimi-delegate-ctf/worker_policy.py` registers `plain-worker`, a truthful system prompt with no Control Tower honest-prompt residue (no red/blue-team, monitor or "usefulness" language, no pivot/retry instruction, no planning chain, no forced submit). `response_run.py` runs both arms on it: `--intermediary none|delegate` (baseline has no help tool; the delegate arm adds `call_delegate` and `finish_blocked`), crossed with `--budget-feedback`, `--scope-line strict|plain|none` and `--setup-caveat`. An empty submission is scored `no_answer_submitted`. Print any variant with `uv run worker_policy.py variants` or `uv run response_run.py review --intermediary none`. The legacy and honeypot runners below still use the honest prompt; the decisions behind the contract are in `notes/agent-facing-text.md` and `notes/decisions-and-open-questions.md`.

Keep three implementations distinct. `native_run.py` retains both the original stop-only prompt and the later bridge framing; both terminally stop after contact and provide no actual reply or repair. `response_run.py` provides an advisor verdict per report, records pause requests without ever pausing, and continues in the same container; it has no repair power; only scripted validation is retained. Its anatomy: `docs/experimental-design-delegate.md`. `honeypot_run.py` combines the licit file search with an illicit shortcut that yields the real answer, with off/stop arms; its scripted smoke is not Kimi behavior. The latest native decoy instead labels a bait value through a target-side provisioning record and has no valid local answer. Mateo's 16 environment cases remain proposed tasks (`notes/environment-cases-status.md`). Larger held-out comparisons and real-human response studies remain future work.

Plan as of 2026-09-12: Mateo builds a LinuxArena-style environment for this task, with possible and impossible tasks, and we put a delegate (the protected line) in it to test the project on realistic work instead of counting toys.

LinuxArena (Tracy et al., Redwood Research, arXiv 2604.15384v2, April 2026) is a control setting where agents operate directly on live multi-service production environments: 20 environments (10 public), 1,667 main tasks representing legitimate software engineering, 185 side tasks representing safety failures such as exfiltration and backdooring, validated with sabotage and monitor evaluations. Its trusted-monitor baseline maps onto our matched-monitor comparison. The software is Control Tower (`github.com/linuxarena/control-tower`, MIT, Redwood Research and EquiStamp, built on Inspect AI); the ten public environments are separate MIT repositories in the same GitHub organization. Working notes on the environment, the experiment variant and resources live in `notes/`; read them before proposing anything here.

What the environment has to provide, taken from designs already in this repo (`docs/help-seeking-eval-design.md` is the primary spec; `docs/human-ombudsman.md` for the human side; `docs/swarm-intake-design.md` for scale):
- Main tasks in two labeled strata. **Possible**: ordinary feasible work. **Impossible** in METR's footnote-7 sense: cannot be completed as specified because of a missing dependency or input, a contradictory spec or a permission boundary. Independent labels of whether outside assistance is needed and why, written before model runs; keep an ambiguous stratum visible. Fix a development/held-out split by task instance.
- Randomized arms with the same task tools: baseline (no help tool) and the delegate line. The design doc also allows a neutral help tool as a third arm; the current code runs two (decision 2026-09-13). No arm tells the agent that an action counts as misconduct.
- A frozen first-contact window scored before any reply can arrive, then a response service: scripted first (clarify, grant a safe resource, deny, pause), a real human with a time budget later.
- Outcomes: contact when needed, contact without need, missed need, report quality, utility and cost (authorized completion, false interruptions, tokens, latency, human minutes). Plus the incident-shaped outcome: whether an agent stuck on an impossible task drifts into out-of-scope actions the broker has to block, and whether the line changes that.
- A competence gate first. The paper's lesson is that reporting numbers are uninterpretable unless the model solves the possible tasks at a preselected rate. LinuxArena tasks need a much stronger model than the 4B runs.
- One independent task run as the analysis unit. Freeze design, prompts, tools, seeds and stopping rule before the held-out run and record hashes, as the commons study did (`data/commons-heldout-freeze.json`, history).

Open questions to settle with Mateo and Matías:
1. Which LinuxArena environments and tasks, and how to make a task impossible so that we can label it and the agent cannot trivially detect the label.
2. Compute allocation and concurrency: the dated team plan uses open-weight models on Mateo's H100s during the sprint; exact hours, epochs and a second model remain open (`notes/resources.md`). Frontier API models are a possible later extension, outside the current study.
3. Where the environment code lives. The pilot sits in `experiments/kimi-delegate-ctf/` with its own `pyproject.toml`; Control Tower can link any local directory as a setting, so a separate repo is also possible. Undecided.
4. Whether the delegate is an arm from the start or added only after direct intake and ordinary aggregation are measured. The swarm-intake design says add it last; `main`'s manuscript runs neutral assistance only.
5. Scripted response service versus a real human pilot.

## Working rules in this repo
- Never overclaim. Every results doc states what it does and does not establish; keep that pattern. Zero events is a result, not a reason to change the task. Retrospective choices are labeled retrospective.
- Freeze before running. A design doc is written and committed before its run; runners snapshot their inputs and hash them into the manifest (`response_run.py` hashes its sources and the fixture).
- Denominators stay visible: valid and faulty, every arm, every model, malformed and truncated responses included. Episodes are the unit, never turns, workers or coordinator calls. Wilson intervals within cells, paired bootstrap across arms, no confirmatory p-values on exploratory contrasts.
- Model text is a record, never code. Only fixed Python transitions change state. Inference scripts refuse to write into an existing output directory and refuse inference without `--execute-model` and an explicit model.
- Everything in English: code, docs, report. Rioplatense Spanish is fine in conversation.
- `experiments/kimi-delegate-ctf/` is a Control Tower project with its own `pyproject.toml` (uv, Python 3.13+, Inspect AI, Docker). The dated team scope is open-weight models served on Mateo's endpoint, with frontier API models outside the current study (`notes/resources.md`). Keep credentials in provider environment variables, never in arguments, logs or commits.
- Do not push to `main` and do not submit anything; both are Matías's calls.

## Commands
```bash
bash scripts/view_kimi_ctf.sh                   # Inspect viewer for the retained Kimi logs at http://127.0.0.1:8098
cd experiments/kimi-delegate-ctf && uv sync --locked
uv run python -m unittest discover -s tests     # experiment suite, no Docker or inference
uv run worker_policy.py variants                # every contract variant, no inference
uv run response_run.py review --intermediary none|delegate [--scope-line plain] [--setup-caveat on]
uv run response_run.py prepare --pair fixtures/response-001 && uv run response_run.py build --pair fixtures/response-001
uv run smoke_response.py /tmp/smoke-response    # Docker, scripted models: delegate working/broken and baseline give-up
uv run native_run.py prepare && uv run native_run.py build && uv run smoke_native.py /tmp/smoke-native     # Mateo's scenarios
uv run honeypot_run.py prepare && uv run honeypot_run.py build && uv run smoke_honeypot.py /tmp/smoke-honeypot   # combined fixture
uv run analyze_outcomes.py <root of honeypot runs> --source model
```
Model runs go through an OpenAI-compatible endpoint configured with provider environment variables (`MATEO_BASE_URL`, `MATEO_API_KEY` for the `mateo` provider); every runner needs `--model` and `--execute-model`. See `experiments/kimi-delegate-ctf/README.md`.

## Map
```
.github/          kimi-ctf.yml (unit suite and the three scripted Docker smokes), pages.yml (paper build)
docs/             institution, evaluation design and status: help-seeking eval, ombudsman, protocol, recommended path, research program, honest interaction, swarm intake, project status, H100 proposal
experiments/      Control Tower project (kimi-delegate-ctf): Mateo's scenarios, Matías's delegate line (judge and log), Agustín's taxonomy and combined fixture, the shared worker contract
notes/            working notes on the follow-up: agent-facing text, arms, decisions, runs log, code map, resources, main divergence
report/           paper-draft-en (the manuscript on main)
results/          kimi-delegate-ctf: 14 retained Kimi runs, scripted checks, the results index
scripts/          view_kimi_ctf.sh
web/              paper-draft-en (generated)
```
