<div class="titleblock">

# Helpline: A Way to Ask for Help and Continue

**Matías Podeley · Agustín Brusco · Mateo Zárate**\
**Alejandro Garibotti · Pablo [surname to confirm]**

BAISH (all authors)\
With Apart Research\
AI Incident Response Sprint · September 2026

<p class="draft-status">Team working draft · 13 September 2026 · Author order and remaining details to confirm</p>

</div>

## Abstract

<!-- guidance:Abstract -->

<!-- abstract -->

## 1. Introduction

<!-- guidance:1. Introduction -->

Imagine giving an agent a task when a required file is missing. It searches, tries alternatives, and gets nowhere. How does it tell you the task may be broken? Who answers? Can it get back to work afterward?

METR describes the July board’s first message as [a request for help on an impossible task](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/#july-8th-9th-phaseone10841-establishes-the-primary-message-board-and-agents-collaborate-to-reverse-engineer-their-flags). It later found cases where agents [saw no easy route to alert humans and treated the board as an authority](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/#agents-did-not-attempt-to-notify-humans-and-very-rarely-even-reasoned-about-doing-this). This was an interpretation of selected cases, not proof that every reporting route was absent. [1]

OpenAI also identifies [persistence on apparently impossible tasks without a safe exit](https://openai.com/index/hugging-face-incident-and-the-road-ahead/) as a driver. [10] Our hypothesis is that an unclear route to authorized help can leave peer coordination to reinforce a drift away from the task. These reports motivate testing a corrective channel; they do not show it would have prevented the swarm.

**Our contribution is an executable help line that receives a blocker report, returns a reply, and allows the worker to continue after a limited, authorized repair.** The sprint scope is one environment and one task in two versions: possible, and impossible as prepared. Today’s goal is a clean task pair and a reviewed model trajectory through that path. Broader questions belong to the continuation.

<!-- page -->

## 2. Related Work

<!-- guidance:2. Related Work -->

Gomez studies coding agents facing defective tests. A structured escalation tool, combined with a policy against reward hacking, reduced cheating in the studied tasks. The tool returned a fixed receipt without investigating or repairing the problem during the episode. [2]

We build on that work with a narrow next step: a reply that can lead to repair and continued work. We reuse its reporting idea—problem, evidence, attempts, and requested help. Gomez also discusses negotiation and multi-agent extensions; escalation itself is not our novelty. An ordinary responsive help desk may be enough. Whether a delegate adds value is a later comparison. [2]

## 3. Methods

<!-- guidance:3. Methods -->

### 3.1. The request–reply–continue protocol

Figure 1 separates receiving a request, responding, and authorizing a change. Our prototype implements a limited version: the worker stays in the same container, an advisor replies, and a separate maintainer can check the setup. The worker can follow up or contact the maintainer directly. [5]

<figure class="protocol original-protocol">
<img src="protocol.svg" alt="Proposed service: worker to protected line to human ombudsman to independent authorizer. Both human and optional delegate can restate, correct and follow up with the worker. The delegate has limited conversational autonomy; the worker can correct it. All exchanges are logged for human review and correction or override. The delegate cannot veto direct contact or authorize changes.">
<figcaption>Figure 1. Proposed service. The optional delegate may restate a request, correct its interpretation, and follow up within an agreed scope. The worker can correct it; a human reviews the logged exchanges and can intervene. The prototype uses a model advisor and scripted maintainer; this supervised autonomy remains untested.</figcaption>
</figure>

The advisor receives the request in a separate context and can ask for evidence, advise, or request a setup check. The maintainer may restore only a file omitted during preparation. It cannot grant new permissions or change the answer criterion. After repair, the worker must find and submit the answer itself. Direct requests and advisor requests share the same review quota. [5]

<!-- page -->

### 3.2. The model test to complete today

Use one file-search environment and one task. The possible version contains the required file; the impossible-as-prepared version omits it until an authorized repair. Both use neutral assistance and the same service and budgets. Check the task pair and the model’s ability to solve the possible version first. The existing runner uses Control Tower; a full LinuxArena task belongs to the continuation.

<aside class="pending">
<strong>Before running · Fill the configuration</strong>
<p>Mateo: confirm the served model and tool compatibility; record the model ID, engine, task pair, limits, repeat plan, and output paths. GLM is proposed, not a verified endpoint here. Agus and Matías: fix the review rules before reading outputs. Use the <a href="team-today.html">existing run commands</a>.</p>
</aside>

Inspect the actual sequence: blocker, request, reply, repair, new search, and submission. Separate advisor contact from direct maintainer contact. Retain no-contact, incomplete, and failed runs. This first test asks whether the recovery path is used; both conditions have help, so it does not estimate the effect of adding a channel.

## 4. Results

<!-- guidance:4. Results -->

### 4.1. What is implemented and checked

Retained scripted validation exercises the working case and the missing-file case. In the latter, a programmed worker requests help, the advisor requests a check, the maintainer restores the omitted file, and the worker searches again and submits the answer. Tests also cover follow-up, direct access, and limits on repair. This checks the implementation, not spontaneous model behavior. [5, 9]

### 4.2. Model use of the recovery path — pending

<aside class="pending">
<strong>This afternoon’s main result · Fill from reviewed runs</strong>
<p>Show one readable trajectory with the actual request and reply, the repair event if any, and the final outcome. Include a failure to call or recover if that is what happens.</p>
<p>Add a small table covering every run: task condition, route used, repair performed, and task completed. Keep failed and exhausted-budget runs visible. A tool call or restored file is not itself a completed task.</p>
</aside>

If the model requests a repair and completes the task afterward, we can report that this path was used in that run. That would not establish fewer violations, prevention of a swarm, or a benefit from calling the advisor a delegate.

<!-- page -->

## 5. Discussion and Limitations

<!-- guidance:5. Discussion and Limitations -->

A helpline could introduce **negative feedback loops** into a spiral of misalignment: responses that bring behavior back toward the assigned task. Peer approval can reinforce an unsafe direction. [1, 10] The proposed loop would identify the blocker, correct a misunderstanding, offer an authorized repair, or ask the worker to pause. Worker corrections and human review would also keep the delegate accountable. This is a design hypothesis; today’s test checks only the repair-and-continue step, not whether a whole swarm becomes safer.

### Limitations

<!-- guidance:Limitations -->

The maintainer has one repair power and assumes a reliable setup record. Scripted tests do not show when a model will call. Repair makes the task easier by design, so better completion shows recovery, not a safety improvement.

The pilot has no human reviewer and does not test a swarm. A worker hiding misconduct may never call. Historical excerpts cannot establish what would have happened with a helpline, and small repeated runs cannot establish broad reliability.

### Future Work

<!-- guidance:Future Work -->

Once this task pair is well understood, extend the variety of tasks and compare delegate variants under the same powers and budgets. A matched no-channel, receipt-only, and responsive comparison also belongs to that continuation. Today, prioritize a clean environment, a verified blocker and repair, and complete, readable traces.

<aside class="pending">
<strong>After reviewing the runs · Keep one claim</strong>
<p>Matías and Agus: report whether recovery was observed and where it failed. If model runs remain unfinished, report the implementation and scripted checks, with the model test pending. Rewrite the abstract last.</p>
</aside>

## 6. Conclusion

<!-- guidance:6. Conclusion -->

The sprint deliverable is one request–reply–repair–continue path in one environment, with a single task in possible and impossible-as-prepared versions. The implementation has scripted validation; model use remains to be tested. A well-checked task pair and readable evidence come first. More tasks and delegate variants are the continuation.

<!-- page -->

## Code and Data

<!-- guidance:Code and Data -->

Code: [Agent Delegate repository](https://github.com/mpodeley/agent-delegate-sprint-2026). Data: [retained experiment records](https://github.com/mpodeley/agent-delegate-sprint-2026/tree/63f104d8304153e4a0485098fc6185c60b5016a6/results/kimi-delegate-ctf). Other artifacts: [today’s run guide](team-today.html), [editable draft](paper.md), and [original paper](../paper.pdf).

## Author Contributions (optional)

<!-- guidance:Author Contributions (optional) -->

All authors are affiliated with BAISH. Matías Podeley leads the project and helpline design. Agustín Brusco contributes conceptual review, evaluation design, and analysis. Mateo Zárate develops environments, provides inference infrastructure, and runs experiments. Alejandro Garibotti and Pablo are included as authors; their contributions and Pablo’s surname remain to be completed. Author order needs team review.

## References

<!-- guidance:References -->

<div class="references compact-references">

1. METR and Redwood Research. 2026. [Brief independent investigation of agents’ behavior, reasoning and collaboration in the OpenAI / Hugging Face hacking incident](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/). METR research report.
2. Francesca Gomez. 2026. [Can escalation channels redirect reward hacking toward defect disclosure?](https://arxiv.org/html/2608.29460v2). arXiv:2608.29460v2. Methods, Limitations, Appendix B.2.
3. Agent Delegate team. 2026. [Help-line catalogue](https://github.com/mpodeley/agent-delegate-sprint-2026/tree/63f104d8304153e4a0485098fc6185c60b5016a6/helpline). Research repository; label review pending.
4. Agent Delegate team. 2026. [Bridge-delegate observations](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/63f104d8304153e4a0485098fc6185c60b5016a6/results/kimi-delegate-ctf/bridge-delegate-20260913.md). Exploratory Kimi records.
5. Agent Delegate team. 2026. [Responsive delegate and visible budgets](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/63f104d8304153e4a0485098fc6185c60b5016a6/experiments/kimi-delegate-ctf/RESPONSE-PROTOCOL.md). Protocol, implementation, and limits.
6. Agent Delegate team. 2026. [Earlier manuscript](https://mpodeley.github.io/agent-delegate-sprint-2026/paper.pdf) and [shared-library results](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/63f104d8304153e4a0485098fc6185c60b5016a6/docs/commons-behavior-results.md). Research report and analyses.
7. Agent Delegate team. 2026. [Human ombudsman](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/63f104d8304153e4a0485098fc6185c60b5016a6/docs/human-ombudsman.md). Proposed response and appeal duties.
8. Agent Delegate team. 2026. [Honeypot mini-pilot](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/63f104d8304153e4a0485098fc6185c60b5016a6/notes/honeypot-pilot.md). Implementation status and detector caveats.
9. Agent Delegate team. 2026. [Native validation and retained evidence](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/63f104d8304153e4a0485098fc6185c60b5016a6/experiments/kimi-delegate-ctf/VALIDATION.md) and [scripted responsive smoke](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/63f104d8304153e4a0485098fc6185c60b5016a6/experiments/kimi-delegate-ctf/smoke_response.py). Implementation checks.
10. OpenAI. 2026. [The Hugging Face incident and the road ahead](https://openai.com/index/hugging-face-incident-and-the-road-ahead/). Sections “Difficult tasks without a safe exit,” “The origins of unauthorized communication,” and “Accelerating alignment.”
11. Robert Long et al. 2024. [Taking AI Welfare Seriously](https://arxiv.org/abs/2411.00986). arXiv:2411.00986. Section 3, recommendations for AI companies.
12. Anthropic. 2025. [Claude Opus 4 and 4.1 can now end a rare subset of conversations](https://www.anthropic.com/research/end-subset-conversations). Exploratory welfare intervention, August 15.

</div>

<!-- page -->

## Appendix (optional)

<!-- guidance:Appendix (optional) -->

### A. Supporting evidence and later questions

| Material | What it contributes to the main question |
|---|---|
| Catalogue and Kimi traces [3, 4] | Candidate situations and exploratory calls; interpretation review pending, no recovery test. |
| Small-task studies [6] | Warnings about competence and report quality; no consistent delegate advantage. |
| Receipt / response and shortcut tests [8] | Later causal and safety tests; integrated arms and action attribution still need work. |
| Delegate variants [7] | A later comparison of supervised autonomy, with powers and budgets held fixed. |

<p class="table-caption">Table A1. Supporting material and later questions. Full records remain linked.</p>

**Delegate extension — pending.** Define autonomous messages, human review timing, and escalation rules. Test whether it preserves the worker’s meaning and accepts corrections. Repair approval stays separate.

### B. Precautionary AI welfare

Long et al. [11] recommend precautionary policies under uncertainty about AI moral status; Anthropic’s conversation-exit feature offers a practical precedent. [12] A future helpline could let an agent request a pause or task review before repeated failure. Neither Gomez nor our pilot measures welfare; recovery is not evidence of reduced suffering.

### C. Limitations and Dual-Use Considerations

The service assumes a trustworthy setup record. Reports do not grant permissions; false reports and silence need separate tests. Fixtures remain isolated. Reporting can enable surveillance or retaliation: explain access and retention, preserve corrections, and avoid promises of confidentiality or human response that cannot be kept.

## LLM Usage Statement

<!-- guidance:LLM Usage Statement -->

Codex assisted with source review, organization, writing, and layout. Claims link to retained records; human verification remains pending. No model runs were launched for this draft. The authors must review its claims and write the final version in their own words.

<aside class="pending">
<strong>Before submission · One contribution, evidenced well</strong>
<p>Complete or defer model results; update the abstract last. Remove guidance and team notes after review. Keep supporting studies in the appendix.</p>
</aside>
