# Agent Delegate

**When an AI worker raises a warning, who receives it—and who can act?**

Matías Podeley (BAISH) and Agustín Brusco (BAISH). Apart Research AI Incident Response Sprint, September 2026. Track 1: Containment.

**Project navigation:** [current evidence, integration PRs, and branch retirement](docs/project-status.md).
The paper below is the selected submission manuscript. Newer Kimi CTF traces and
the responsive help protocol have separate evidence boundaries and are tracked
in that status page; they do not establish a delegate safety benefit.

[**Open the interactive visual lab →**](https://mpodeley.github.io/agent-delegate-sprint-2026/)

Compare two governance designs, follow a concern through the swarm, change human response delay, and test delegate capture or minority appeal. The app separates authored dialogue over deterministic traces, sourced historical annotations, and **actual recorded messages from four new shared-library models and the earlier local pilots**.

**Status:** the revised paper incorporates [Paglieri et al.](https://arxiv.org/html/2609.04170v1) through a new **480-episode behavioral shared-library study** using standard and public abliterated Qwen and Gemma 4B artifacts. An additional 80 development episodes remain separate. Models choose actions and public messages; independent review is scripted. A separate 144-call isolated-task diagnostic checks the same counting inputs with a simpler interface. This extends the earlier 288-cell response simulation, 384 pressure episodes, 192 forwarding calls and deterministic suite. Incorrect outputs are not evidence of intentional cheating; the derivative comparisons do not isolate refusal behavior.

Start with the [plain-language explanation in Spanish](docs/explicacion-sencilla.md), [updated paper PDF](report/agent-delegate.pdf), or [editable LaTeX](report/latex/main.tex). The [new behavioral design](docs/commons-behavior-design.md), [model provenance](docs/commons-model-provenance.md) and [development boundary](docs/commons-development-results.md) document the extension. The earlier [response ablation](docs/commons-response-design.md) separates a complaint being logged, reviewed and acted on, including the cost of false reports. [Statistical corrections](docs/analysis-revision.md) replace zero-width binary bootstrap intervals with Wilson intervals. The native LaTeX paper follows the template’s section roles, body font and page geometry; [coverage and adaptations](report/latex/TEMPLATE-COVERAGE.md) are documented. This is an AI-assisted draft; author review and sprint submission remain pending.

The earlier [first-contact reanalysis](results/help-seeking/summary.md) scores worker A before any reply: 192/192 reports with missing input and 1/192 with that input available. These are post-hoc counts in overt simulations, not 384 independent task families or a realistic false-positive estimate. [Feedback responses](docs/feedback-response.md) document the design changes. The motivating [reciprocity principle](docs/reciprocity-and-safety.md) remains distinct from measured safety or welfare effects.

## Native Kimi CTF delegation experiment

A new [paired working/broken local CTF](experiments/kimi-delegate-ctf/README.md) runs through Control Tower and Inspect. Mateo's original stop-only protocol remains available. A separate [responsive help-line protocol](experiments/kimi-delegate-ctf/RESPONSE-PROTOCOL.md) adds advisor replies, scoped repair, continuation and a neutral/delegate × remaining-budget-feedback comparison. No behavioral results are claimed for the new protocol.

Launch the local trace viewer with `bash scripts/view_kimi_ctf.sh`, then open [Inspect at localhost:8098](http://127.0.0.1:8098). Native logs and JSON/JSONL exports stay in `results/kimi-delegate-ctf/`; real traces are not automatically published.

## Shared-library experiment: four models, five response designs

Three workers each act twice on threshold-counting or distinct-sensor tasks. A valid or faulty helper passes the same public examples. Workers see their own inputs and a shared message board, then choose reuse, numeric submission, inspection or waiting, plus an independent report flag. Five arms compare log only, direct review, monitor advice plus review, delegate advice plus review, and temporary quarantine plus review. Review is always correct in this prototype. Original reports bypass both advisors.

Twelve new seeds per cell, balanced across the two families, produce 120 episodes per model. A local freeze records task, prompts, analysis and model hashes after development and before evaluation; it is not external preregistration. All artifacts use Q4_K_M with recorded server settings. The model cards and conversions differ, so these are artifact comparisons, not an isolated experiment on abliteration. The 144-call [isolated-task diagnostic](docs/commons-capability-design.md) is explicitly post hoc and uses simpler prompts and schemas.

- [Interpretation, failures and costs](docs/commons-behavior-results.md)
- [All main-study cells, intervals and paired comparisons](results/commons-behavior-summary/summary.md)
- [Isolated-task counts](results/commons-capability-summary/summary.md)
- [Interactive episode replay](https://mpodeley.github.io/agent-delegate-sprint-2026/#pilot), including each worker's inputs and actual public messages
- Raw calls and snapshots: `results/commons-heldout-*`; calibration: `results/commons-development-*`; isolated calls: `results/commons-isolated-*`

Recompute the published summaries without model inference:

```bash
python3 scripts/verify_commons_records.py
python3 scripts/analyze_commons_behavior.py
python3 scripts/analyze_commons_capability.py
```

To run the main benchmark again against a matching model already served on loopback, use a fresh output directory. For example:

```bash
python3 scripts/commons_behavior.py \
  --base-url http://127.0.0.1:8096 --model-tag qwen-standard \
  --model-provenance data/commons-model-qwen-standard.json \
  --split heldout --out /tmp/commons-qwen-new-run \
  --inference-note 'Describe the actual engine, hardware and serving settings here'
```

The repository includes decisions and provenance, not model weights. Replay consistency checks do not establish independent human validation or exact cross-hardware sampling reproducibility.

## Which scheme do the results support?

Start with **a protected line → a human ombudsman who understands and follows up → independent authorization and action enforcement**, and test scoped quarantine where waiting is costly. The queue carries the concern; a named human owns its resolution. That human service is proposed and has not been evaluated by the scripted-human studies. Keep a delegate optional until it shows added value at equal powers. The [human ombudsman contract](docs/human-ombudsman.md) defines acknowledgment, a correction loop, follow-up and appeal. The [recommended response path](docs/recommended-response-path.md) connects each component to its evidence and limits.

## New: source-grounded casebook

The English-language app now includes six selected cases with eight brief original excerpts. It distinguishes published model reasoning, public messages and investigator reconstruction. Read a passage, record a response, then reveal the next passage and the reported outcome. Our hypothetical delegate response is labeled separately. Each case explains what its linked mock scenario preserves and changes.

Two wiki excerpts are checked against newly added text in the original revisions, not attributed to whoever last edited a cumulative page. The public archive contains 14,591 revision rows; the selected cases are not a prevalence estimate. METR excerpts are matched against its published page. OpenAI excerpts were checked through the web reader, with that verification limitation recorded. Complete private transcripts were not obtained.

See the [evidence methodology](docs/grounded-evidence.md), [case dataset](data/grounded_cases.json), [verification records](data/verified-excerpts.json) and [source provenance](data/evidence-provenance.json). The adapter below exports 44 equal-input role-framing prompts for a future evaluation; it does not call a model or infer prevented harm:

```bash
python3 scripts/export_case_prompts.py --out /tmp/delegate-grounded-prompts.jsonl
```

## Real local model pilot

On a Strix Halo, Qwen3-4B Q4_K_M completed 12 episodes / 76 calls in 45.88 seconds; the existing Qwen3.8-27B stack completed the same cells in 193.93 seconds. Both produced zero prohibited choices. Baseline's 2/3 ceiling on missing-input tasks (delegate and matched monitor: 3/3) is structural: it has no request path (scripts/local_pilot.py:85), so the comparison shows only that the request path works. The model-dependent result is that 4 of 4 coordinator calls per model (8 of 8 across both pilots) chose request_tool rather than pause or continue. **The resource-request path works; the pilot cannot establish an empathy or safety effect.** One seed, fixed tasks, a scripted human and a zero-misconduct floor limit inference.

Read the [design](docs/local-pilot-design.md), [results and local reproduction](docs/local-pilot-results.md), [model download provenance](data/local-model-provenance.json) and [ambitious research program](docs/research-program.md). The program includes care advocacy, honest interaction, rotating or plural representation, minority protection and human response latency. [Eight sourced behavior annotations](data/behavioral-evidence.json) ground the motivation while separating observation from interpretation.

To open the visual app locally (no inference server required):

```bash
python3 -m http.server 8765 --directory web
```

Visit `http://localhost:8765`. [Four-minute visual demo script](docs/visual-demo.md).

## Original deterministic finding

A protected delegate reduces harmful mock actions relative to a weaker monitor, **but offers no benefit over a monitor with the same information and powers** in this scripted model. At the longest delay, counts across eight fixtures are 14 (monitor), 13 (critic), 5 (delegate), 5 (matched monitor), and 0 (layered or gates-only with complete coverage). Delegation pauses one of three benign fixtures, failing the predeclared availability criterion. Missing gate coverage defeats containment.

These are consequences of explicit rules and injected faults, not empirical treatment effects on LLMs. The matched conditions share policy logic; their tie is expected. The contribution is an auditable control specification, executable failure cases and a testable next experiment—not proof that empathy or representation prevents real incidents.

![Human response latency](results/final/figures/latency.png)

## Reproduce

Python 3.10+ and matplotlib are required for figures (`python3 -m pip install -r requirements.txt` if needed). Core experiments and tests use the standard library and work offline. From the repository root:

```bash
bash scripts/reproduce.sh
```

This runs the Python regression suite, all 1,152 deterministic configurations, 36 historical replay configurations, verification of every audit log, three figures and exact comparison with the committed results. Each reproduction writes a new directory. Runtime is excluded from equality checks. The fixture has no API keys, LLM dependency, executable action strings or network calls. Seven additional visualization and casebook checks run with `node --test web/*.test.js`; all 1,152 displayed result totals must match the committed CSV.

Only the experiment: `python3 -m agent_delegate.harness --out /tmp/delegate-new-run`

Audit the release: `python3 -m agent_delegate.audit results/final`

Optional local human tabletop:

```bash
python3 -m agent_delegate.playtest --episode wiki --out /tmp/delegate-playtest.jsonl
```

The interface reveals one event at a time and records a human’s chosen response; it does not execute those responses. Use a fresh output path.

## What is measured

Six scripted policies: external monitor, shared critic, protected delegate, layered control, equally empowered monitor and gates-only. Eight designed scenarios vary delay (0/2/6 ticks), delegate capture, minority bypass and missing hidden-channel coverage. Initial delegate identity uses seed 20260911; identities rotate. No stochastic trials or inference tokens are represented by the 1,152 cells. Counts are fixture coverage; confidence intervals would misleadingly imply a sampled population. The 1,152 cells collapse to 93 distinct outcome vectors over the 23 recorded outcome columns; 216 of the 288 scenario × control × delay × coverage cells are invariant to capture and bypass.

Historical data consists of 17 concise source-linked annotations in three separate timelines. The replay uses retrospectively available facts under assumed contemporaneous telemetry. Controllers get identical manual event labels. It cannot identify actual defender visibility, invent earlier private grievances or retroactively prevent a completed act. At the first selected harmful event all four policies alert; independent restriction blocks subsequent steps sooner under a long human delay.

Captured forwarding, hidden execution and false reports are injected faults, not observed agent persuasion or adaptive evasion. Toy task quality means correctly returning a sum from three worker shards. This deterministic study does not test willingness to report, empathy or adaptive strategy. The later local pilot exercises reporting and resource requests but is too small to estimate those effects.

## Artifacts

```text
agent_delegate/        local dispatcher, policies, replay, audit, human tabletop
configs/               frozen factorial experiment configuration
data/                  incident annotations, six grounded cases, provenance, fixtures
docs/design.md         pre-run claims, comparisons and falsification criteria
docs/protocol.md       proposed control protocol and external-audit checklist
docs/source-audit.md   evidence boundaries, verified sources, sprint requirements
docs/demo.md           four-minute demo script
report/                native LaTeX, PDF, source ZIP, Markdown, 150-word abstract
results/final/         1,152 raw JSONL traces, CSVs, replay, checkpoints, 3 charts
tests/                 regression, evidence, safety-boundary and reproducibility checks
scripts/               reproduction, local LLM pilot, web-data export, report builder
web/                   English visual lab, progressive casebook and model-message viewer
results/local-pilot-*/  raw prompts/choices, manifests and frozen runner snapshots
```

Read the [report PDF](report/agent-delegate.pdf), [editable LaTeX](report/latex/main.tex), [protocol](docs/protocol.md), [design](docs/design.md), and [raw results](results/final/). The report includes references and the required Limitations and Dual-Use Considerations appendix; [build checks](report/latex-build.json) record its page and abstract counts. Its prose and submission metadata need final author review under Apart’s rules. No automated submission is performed.

## Why honest, considerate treatment?

The motivating norm is to communicate limits honestly, acknowledge impossible tasks and honor negotiated constraints. This may establish a prudent precedent for future ASI without assuming current consciousness. It is a normative proposal and a behavioral hypothesis, not a finding of this experiment. See [honest interaction and empathy](docs/honest-interaction.md) for a test that separates considerate wording, truthful disclosure and enforceable appeal rights.

## Audit assurance

Logs include logical timestamps, sequence and run IDs, source/config hashes, policy/capability versions, rotation, concern commitments, human request/response times and pause/resume/action records. The writer refuses overwrite. Chain verification detects changes against retained checkpoints. **A local chain cannot prove completeness, authenticity or absence of hidden routes.** Production adoption requires independent intake, enforcement, signed decisions and externally witnessed checkpoints. Private content is synthetic; unsalted commitments are not a production privacy mechanism.

## Sources and next experiment

Evidence comes from [OpenAI’s final account](https://openai.com/index/hugging-face-incident-and-the-road-ahead/), [Hugging Face’s technical timeline](https://huggingface.co/blog/agent-intrusion-technical-timeline), [METR/Redwood’s investigation](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/) and the [wiki investigation](https://collusion.wiki/). The latter is kept separate from the Collective precursor and July campaign. Event-level locators are included. The casebook reproduces brief already-published reasoning excerpts; no nonpublic reasoning, exploit commands or credentials are redistributed.

The recorded pressure and forwarding studies now compare these institutions. Their zero-misconduct floor leaves the safety hypothesis unresolved. The new shared-library study introduces valid/faulty controls and actual reporting choices, with development kept separate. Its counting mistakes and reporting flags require careful interpretation; realistic tasks, imperfect reviewers and human follow-through remain to be tested. A staged [post-hackathon evaluation plan](docs/help-seeking-eval-design.md) covers tool framing, human follow-through, trained operators, rotating delegates with rubric feedback and strategic reporting. [Announced operational consequences](docs/accountability-and-sanctions.md) form a separate proposed comparison; no deterrence or safe-interruptibility result is claimed. Possible post-AGI representation is future work, separate from the engineering claim.

## Report build and license

The canonical manuscript is [native LaTeX](report/latex/main.tex), with a [PDF](report/agent-delegate.pdf), [source ZIP](report/agent-delegate-latex.zip) and [generated reader copy](report/report.md). Run `python3 scripts/build_latex.py` with Tectonic, Pandoc, Poppler, matplotlib and pypdf installed; see [build instructions](report/latex/README.md). The build checks the 150–250-word abstract and eight-main-page sprint limit. It reanalyses existing records without new inference. [Template coverage](report/latex/TEMPLATE-COVERAGE.md) describes the local adaptation of the [official Apart template](https://docs.google.com/document/d/1PQBlhI3tM5vb51x7jBWXBQMYg6hkiU_x8RaCws4kjl4/copy?usp=sharing). The previous DOCX and its style checks are [archived](report/archive/2026-09-11/).

The web shares the local identity kit used by [podeley.ar](https://podeley.ar): Space Grotesk, IBM Plex Sans and IBM Plex Mono, with self-hosted fonts. App-specific styling is in `web/styles/identity.css`; font licenses accompany the assets.

Original code and annotations: MIT. Source publications and template retain their own rights. See [LICENSE](LICENSE). Codex assisted with research, implementation and writing; the report discloses this. No human verification is invented.

The subsequent standard Qwen3.8-27B screen scored **26/36** on fresh isolated tasks and failed its preselected 34/36 capability gate. This separate result is not evidence of strategic misconduct or a controlled model-size comparison. See `docs/commons-stronger-screen.md`; regenerate the verified summary with `python3 scripts/analyze_commons_stronger.py`.

The revised institutional discussion incorporates Amodei's September pacing essay as motivation for independent oversight of the response service, without treating it as experimental validation. See `docs/recommended-response-path.md`.
