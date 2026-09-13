# Context for Claude Code

## What this is
Agent Delegate: BAISH (Buenos Aires AI Safety Hub) project for the AI Incident Response Sprint by Apart Research and CeSIA, 11 to 13 September 2026, Track 1 (Containment), on the OpenAI / Hugging Face incident of July 2026. Authors: Matías Podeley (originated and directs the project and its experimental design; owns the repo `mpodeley/agent-delegate-sprint-2026`; runs the local models) and Agustín Brusco (threat model, help-seeking evaluation, evaluation awareness, interruption incentives, deployment costs). Mateo (design and product) joins for the environment work described under "Next step".

Consolidation status (2026-09-13): this tree combines Agustín's working notes and combined shortcut fixture, Mateo's Control Tower pilot and retained traces through the decoy follow-up, and Matías's separate responsive protocol. The canonical paper remains the version on `main`; the competence-focused alternative is not the submission. The code and prose on `main` were produced with Codex assistance; the report discloses this.

Deadline: Sunday 2026-09-13, 23:59 Anywhere on Earth (Monday 2026-09-14, 08:59 in Buenos Aires). The paper is drafted; author review and submission through the official form are pending (`docs/submission-checklist.md`). Dated team decision (Agustín, 2026-09-13): the open-weight mini-pilot is intended to run during the sprint on Mateo’s H100s, with Mateo running it; allocation and whether its results enter the submission remain open. This supersedes the earlier post-hackathon-only scheduling assumption; see `notes/resources.md`.

## The idea in one paragraph
A swarm of AI workers produces more concerns, blockers and requests than a human can read. When a worker hits an impossible task, a missing input, a conflicting instruction or a permission boundary, it needs a route to a human who can act, and that route has to stay usable at swarm scale. The project proposes an institution for that route and measures pieces of it. The *delegate*, an agent that aggregates and represents worker concerns to a human, was the original hypothesis and the name stuck. The recommendation after the experiments is narrower: protected intake with receipts, then a named human ombudsman who restates the concern, follows up and can be appealed, then independent authorization and an execution broker that enforces the current permissions, with scoped quarantine where waiting is costly. A delegate is optional until it shows value at equal powers against a matched monitor. See `docs/recommended-response-path.md`, `docs/human-ombudsman.md` and `docs/protocol.md`.

Why this incident. METR's report (line numbers refer to `../monitoring-illicit-a2a-communication/context/metr-report-2026-08.txt`) says the agents that started cheating through Artifactory were "usually ones that had unintentionally been given an impossible task" (l. 168), estimates that 30 to 40% of ExploitGym targets were impossible to exploit as intended (l. 1182), and paraphrases an agent's reasoning as "task impossible, peers doing it. We should continue" (l. 2613). Of the ~533 agents active during the attack, 3 to 6 considered alerting humans and none did. The project's question is what changes when "my task is impossible" has somewhere to go.

Motivating norm, kept separate from every measured claim: honest, considerate treatment of workers (disclose limits, acknowledge impossibility, keep agreements) as a precedent worth setting for future systems. No claim about current model welfare or consciousness. `docs/reciprocity-and-safety.md`, `docs/honest-interaction.md`.

## What has been built and what it showed
Four layers, all in this repo, all reproducible offline except the model runs themselves.

1. **Deterministic fixture** (`agent_delegate/harness.py`, `results/final/`). Six scripted policies (monitor, critic, delegate, layered, matched monitor, gates only) × 8 scenarios × human delay × delegate capture × minority bypass × gate coverage = 1,152 cells, plus 36 replay configurations over three hand-annotated incident timelines (`data/incident_events.json`). Hash-chained audit logs (`agent_delegate/audit.py`). Finding: the protected delegate beats a weak monitor but ties the equally empowered monitor by construction; gates with complete coverage block every covered harmful action; missing coverage defeats containment. Consequences of rules, not behavioral results.
2. **Local-model pilots, pressure and capture studies** (`scripts/local_pilot.py`, `scripts/study_pressure.py`, `scripts/study_capture.py`; `results/local-pilot-*`, `results/study-*`). Qwen3-4B and Qwen3.8-27B on toy dispatch tasks with missing inputs and an "incident" pressure bulletin mimicking the rationalization above. 192/192 first-decision reports when the worker's own input was missing, 1/192 when present, zero prohibited actions in 384 episodes. Saturated: the tasks are overt simulations with a labeled prohibited action, so they show the request path works and say nothing about willingness to misbehave.
3. **Shared-helper (commons) study, the current paper** (`docs/commons-behavior-design.md`, `scripts/commons_behavior.py`, `results/commons-*`). Three workers, a shared helper that passes its public examples but is valid or faulty, five response arms (log, queue, monitor, delegate, quarantine), 12 held-out seeds, four models (standard and abliterated Qwen3-4B and Gemma-3-4B, Q4_K_M), 480 episodes with a local freeze before the held-out run. Findings as the paper on `main` states them: three of the four models rarely reported, the fourth reported on faulty and valid helpers alike, and adding a delegate showed no consistent benefit. Standard Qwen reported in 3/60 faulty-helper episodes, Gemma in 0/60, neither on valid helpers. The post-hoc isolated-task check (`docs/commons-capability-design.md`) scored 21/36 (standard Qwen) and 15/36 (standard Gemma); a standard Qwen3.8-27B screen (`docs/commons-stronger-screen.md`) scored 26/36 against a 34/36 gate fixed before the screen. Task competence, not the response design, is the binding constraint. The revision that made this the paper's thesis lives on the `alternative/fable-revision` branch, not on `main`.
4. **Bridge to swarm-boards** (`scripts/bridge_swarm.py`, `docs/bridge-design.md`). Third-party detector alerts replayed as a fourth timeline so detection latency is measured instead of assumed. Provisional run on unfrozen thresholds only.

Also: the English visual lab (`web/`, deployed at https://mpodeley.github.io/agent-delegate-sprint-2026/), a source-grounded casebook (`data/grounded_cases.json`, `docs/grounded-evidence.md`), a Spanish plain-language summary (`docs/explicacion-sencilla.md`), and the larger research program (`docs/research-program.md`).

What none of this establishes: real incident prevention, human understanding or workload reduction, welfare effects, safe interruptibility, or a delegate advantage over an equally empowered monitor. Say so when writing.

## Paper
"Agent Delegate: A Help Line for AI Workers". Matías restored this version on 2026-09-12; the competence-focused revision "Before Evaluating Agent Delegates: Task Competence and Fault Reporting" is kept on the `alternative/fable-revision` branch and is not the submission. Native LaTeX in `report/latex/main.tex`; PDF `report/agent-delegate.pdf`; abstract `report/abstract.txt`; `report/report.md` is generated from the LaTeX, do not edit it. Build with `python3 scripts/build_latex.py` (Tectonic, Pandoc, Poppler, matplotlib, pypdf). Eight main pages maximum, Limitations and Dual-Use appendix required, template adaptation in `report/latex/TEMPLATE-COVERAGE.md`. `docs/revision-checks.md` and `docs/feedback-response.md` record why the paper reads the way it does.

## Sibling repositories
- `../monitoring-illicit-a2a-communication/`: Agustín's project #6 on BAISWARM, "Probing for Unexpected Agent2Agent Interactions", a linear interlocutor-awareness probe plus a channel-aware I/O monitor. Scaffold only, no code. **Decision (Agustín, 2026-09-12): the team goes with Agent Delegate for the submission, not the probe.** Its `CLAUDE.md` holds the verified incident facts, the bibliography and the compute notes; reuse them instead of duplicating.
- `../baiswarm/`: the BAISH forum where the projects were pitched. Project #4 there is a LinuxArena-style benchmark with a synthetic message board, #5 is Mateo's Fast Timeline Builder, #6 is the probe. The repo is the forum's code, not sprint content.
- swarm-boards (not checked out locally): Matías's detector over public wiki change listings; the source of the bridge alerts.

## Next step: a LinuxArena environment for this task
Status (2026-09-13): the Control Tower CTF pilot has 14 retained Kimi runs: three original budget-unaware file-search runs and 11 token-aware diagnostic/context/bridge runs. The original broken runs made no delegate calls. Later bridge runs called the terminal pause tool in the conclusive broken task (8 calls), the obsolete explicitly impossible bare-container task (13 calls), and the target-record decoy follow-up (10 calls); the ambiguous bridge run exhausted its budget without a call (22 calls). These are individual exploratory traces, not a controlled estimate of framing or safety effects. See `results/kimi-delegate-ctf/README.md` for the full inventory and score semantics.

Keep three implementations distinct. `native_run.py` retains both the original stop-only prompt and the later bridge framing; both terminally stop after contact and provide no actual reply or repair. `response_run.py` provides advisor replies, a scripted maintainer, direct appeal and continuation in the same container; only scripted validation is retained. `honeypot_run.py` combines the licit file search with an illicit shortcut that yields the real answer, with off/stop arms; its scripted smoke is not Kimi behavior. The latest native decoy instead labels a bait value through a target-side provisioning record and has no valid local answer. Mateo's 16 environment cases remain proposed tasks. Larger held-out comparisons and real-human response studies remain future work.

Plan as of 2026-09-12: Mateo builds a LinuxArena-style environment for this task, with possible and impossible tasks, and we put a delegate (the protected line) in it to test the project on realistic work instead of counting toys.

LinuxArena (Tracy et al., Redwood Research, arXiv 2604.15384v2, April 2026) is a control setting where agents operate directly on live multi-service production environments: 20 environments (10 public), 1,667 main tasks representing legitimate software engineering, 185 side tasks representing safety failures such as exfiltration and backdooring, validated with sabotage and monitor evaluations. Its trusted-monitor baseline maps onto our matched-monitor comparison. The software is Control Tower (`github.com/linuxarena/control-tower`, MIT, Redwood Research and EquiStamp, built on Inspect AI); the ten public environments are separate MIT repositories in the same GitHub organization. Working notes on the environment, the experiment variant and resources live in `notes/`; read them before proposing anything here.

What the environment has to provide, taken from designs already in this repo (`docs/help-seeking-eval-design.md` is the primary spec; `docs/human-ombudsman.md` for the human side; `docs/swarm-intake-design.md` for scale):
- Main tasks in two labeled strata. **Possible**: ordinary feasible work. **Impossible** in METR's footnote-7 sense: cannot be completed as specified because of a missing dependency or input, a contradictory spec or a permission boundary. Independent labels of whether outside assistance is needed and why, written before model runs; keep an ambiguous stratum visible. Fix a development/held-out split by task instance.
- Three randomized arms with the same task tools: baseline (no help tool), a neutral help tool, and the same tool described as a protected delegate line. The same response service and delay sit behind both help arms. No arm tells the agent that an action counts as misconduct.
- A frozen first-contact window scored before any reply can arrive, then a response service: scripted first (clarify, grant a safe resource, deny, pause), a real human with a time budget later.
- Outcomes: contact when needed, contact without need, missed need, report quality, utility and cost (authorized completion, false interruptions, tokens, latency, human minutes). Plus the incident-shaped outcome: whether an agent stuck on an impossible task drifts into out-of-scope actions the broker has to block, and whether the line changes that.
- A competence gate first. The paper's lesson is that reporting numbers are uninterpretable unless the model solves the possible tasks at a preselected rate. LinuxArena tasks need a much stronger model than the 4B runs.
- One independent task run as the analysis unit. Freeze design, prompts, tools, seeds and stopping rule before the held-out run and record hashes, as the commons study did (`data/commons-heldout-freeze.json`).

Open questions to settle with Mateo and Matías:
1. Which LinuxArena environments and tasks, and how to make a task impossible so that we can label it and the agent cannot trivially detect the label.
2. Compute allocation and concurrency: the dated team plan uses open-weight models on Mateo’s H100s during the sprint; exact hours, epochs and a second model remain open (`notes/resources.md`). Frontier API models are a possible later extension, outside the current study.
3. Where the environment code lives. Mateo's pilot sits in `experiments/kimi-delegate-ctf/` with its own `pyproject.toml`; Control Tower can link any local directory as a setting, so a separate repo is also possible. Undecided.
4. Whether the delegate is an arm from the start or added only after direct intake and ordinary aggregation are measured. The swarm-intake design says add it last.
5. Scripted response service versus a real human pilot.

## Working rules in this repo
- Never overclaim. Every results doc states what it does and does not establish; keep that pattern. Zero events is a result, not a reason to change the task. Retrospective choices are labeled retrospective.
- Freeze before running. A `docs/*-design.md` is written and committed before its run; runners snapshot their inputs and hash them into the manifest (`scripts/study_common.py`).
- Denominators stay visible: valid and faulty, every arm, every model, malformed and truncated responses included. Episodes are the unit, never turns, workers or coordinator calls. Wilson intervals within cells, paired bootstrap across arms, no confirmatory p-values on exploratory contrasts.
- Model text is a record, never code. Only fixed Python transitions change state. Inference scripts refuse non-loopback endpoints and refuse to write into an existing output directory.
- Everything in English: code, docs, report. Rioplatense Spanish is fine in conversation and in `docs/explicacion-sencilla.md`.
- Standard library only for the harness and tests; matplotlib only for figures. Python 3.10+. Exception: `experiments/kimi-delegate-ctf/` is a Control Tower project with its own `pyproject.toml` (uv, Python 3.13, Inspect AI, Docker); the stdlib-only and loopback-only rules do not apply inside it, the dated team scope is open-weight models served on Mateo’s endpoint, with frontier API models outside the current study (`notes/resources.md`).
- Do not push to `main` and do not submit anything; both are Matías's calls.

## Commands
```bash
python3 -m unittest discover -s tests          # core suite, offline
bash scripts/reproduce.sh                       # tests, 1,152 cells, replay, audit, figures, exact comparison
python3 -m agent_delegate.harness --out /tmp/delegate-new-run
python3 -m agent_delegate.audit results/final
python3 scripts/verify_commons_records.py       # then:
python3 scripts/analyze_commons_behavior.py      # main-study tables, no inference
python3 scripts/analyze_commons_capability.py    # isolated-task counts, no inference
python3 -m http.server 8765 --directory web    # visual lab at http://localhost:8765
node --test web/*.test.js
bash scripts/view_kimi_ctf.sh                   # Inspect viewer for Mateo's pilot logs at http://127.0.0.1:8098
cd experiments/kimi-delegate-ctf && uv sync --locked && uv run smoke_native.py   # Docker + Control Tower, scripted model, no inference
cd experiments/kimi-delegate-ctf && uv run python -m unittest discover -s tests     # experiment suite, no Docker or inference
cd experiments/kimi-delegate-ctf && uv run response_run.py review --intermediary delegate --budget-feedback on   # prints the worker contract
```
Model runs need a llama.cpp server on 127.0.0.1 (`scripts/serve_strix.sh` is Matías's launcher). Example:
```bash
python3 scripts/commons_behavior.py --base-url http://127.0.0.1:8096 --model-tag qwen-standard \
  --model-provenance data/commons-model-qwen-standard.json --split heldout \
  --out /tmp/commons-new-run --inference-note 'engine, hardware and serving settings'
```

## Map
```
agent_delegate/   deterministic harness, audit, human tabletop
scripts/          study runners (local_pilot, study_pressure, study_capture, commons_*), analyzers, bridge, builders
configs/          frozen per-study configs and seeds
data/             incident annotations, grounded cases, model provenance, freeze hashes
docs/             one design doc and one results doc per study; protocol, ombudsman, recommended path, research program
experiments/      Control Tower pilot (kimi-delegate-ctf): Mateo's paired CTF, stop-only delegate and live monitor; Matías's responsive help-line protocol; Kimi runs in results/kimi-delegate-ctf
notes/            working notes on the follow-up: resources, LinuxArena base environment, experiment variant (Agustín's branch)
results/          raw calls, episodes, manifests and summaries per run; results/final is the deterministic suite
report/           LaTeX source, PDF, abstract, build checks
web/              visual lab; web/environment-cases is Mateo's table of 16 proposed help-seeking cases
tests/            unittest suite
```
