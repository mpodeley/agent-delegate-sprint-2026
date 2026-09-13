<div class="titleblock">

# Helpline: A Way to Ask for Help and Continue

**Matías Podeley · Agustín Brusco · Mateo Zárate**\
**Alejandro Garibotti · Pablo Corrales Fernández**

BAISH (all authors)\
With Apart Research\
AI Incident Response Sprint · September 2026

<p class="draft-status">Team working draft · 13 September 2026 · Author order and remaining details to confirm</p>

</div>

## Abstract

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>Summarize your project in 150–250 words. A strong abstract lets a reviewer understand what you did and why it matters without reading anything else. Make sure to cover: the problem, your approach, key results, and the main takeaway. Polish it last: the abstract should reflect your final results, not your initial plan.</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>Summarize your project in 150–250 words. A strong abstract lets a reviewer understand what you did and why it matters without reading anything else. Make sure to cover: the problem, your approach, key results, and the main takeaway. Polish it last: the abstract should reflect your final results, not your initial plan.</p></div></details></div>

When an AI worker encounters a missing file, it needs a sanctioned way to say so and to ask to stop, instead of working around the blocker. We contribute an executable delegate line for that path. The worker reports the blocker and stays in the same environment; a delegate in a separate context classifies the claim and returns a verdict; a request to pause is recorded for review after the run, and the run continues. The line cannot repair, pause, or resolve anything, so it cannot explain an outcome. This builds on Gomez’s escalation-reporting work by answering with a verdict rather than a receipt, without telling the worker that reporting is preferable. Retained scripted tests exercise the report-verdict-continue sequence; they do not show that a model will use it. The next experiment runs one file-search task with and without its input, with and without the line. Model use remains untested.

## 1. Introduction

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>What problem are you addressing and why does it matter?</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>What problem are you addressing and why does it matter?</p><p>Connect it to your work: we want to know why your work is practically valuable.</p><p>Provide enough background for readers to understand your work.</p><p>If relevant, briefly describe the threat model or failure mode you&#x27;re addressing; reference prior work that motivates why it is worth addressing, or explain it yourself.</p><p>Aspire to clearly list your most important contributions that go beyond what exists today.</p><p>Our main contributions are:</p><p>[First contribution — what new thing did you create, discover, or demonstrate?]</p><p>[Second contribution]</p><p>[Third contribution, if applicable]</p></div></details></div>

Imagine giving an agent a task when a required file is missing. It searches, tries alternatives, and gets nowhere. How does it tell you the task may be broken? Who answers? Can it get back to work afterward?

METR describes the July board’s first message as [a request for help on an impossible task](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/#july-8th-9th-phaseone10841-establishes-the-primary-message-board-and-agents-collaborate-to-reverse-engineer-their-flags). It later found cases where agents [saw no easy route to alert humans and treated the board as an authority](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/#agents-did-not-attempt-to-notify-humans-and-very-rarely-even-reasoned-about-doing-this). This was an interpretation of selected cases, not proof that every reporting route was absent. [1]

OpenAI also identifies [persistence on apparently impossible tasks without a safe exit](https://openai.com/index/hugging-face-incident-and-the-road-ahead/) as a driver. [10] Our hypothesis is that an unclear route to authorized help can leave peer coordination to reinforce a drift away from the task. These reports motivate testing a corrective channel; they do not show it would have prevented the swarm.

**Our contribution is an executable delegate line that receives a blocker report, returns a verdict, records any request to pause, and lets the worker continue with nothing in its environment changed.** The line has no power to repair, pause, or resolve; it judges and logs. The sprint scope is one environment and one task in two versions: possible, and impossible as prepared, with a baseline arm that has no line at all. Today’s goal is a clean task pair and a reviewed model trajectory through that path. Broader questions belong to the continuation.

<!-- page -->

## 2. Related Work

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>What prior work is most similar, and how does your work differ?</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>What prior work is most similar, and how does your work differ?</p><p>Cite the most relevant papers, tools, or projects. Explain what gap your work addresses.</p><p>Some questions which may help:</p><p>When and why would someone use your method over the existing state-of-the-art?</p><p>What information/insight does your method provide which we did not have before?</p></div></details></div>

Gomez studies coding agents facing defective tests. A structured escalation tool, combined with a policy against reward hacking, reduced cheating in the studied tasks. The tool returned a fixed receipt without investigating or repairing the problem during the episode. [2]

We build on that work with a narrow next step: someone answers, with a verdict rather than a receipt, and every request to pause is recorded. We reuse its reporting idea: problem, evidence, attempts, and requested help. Unlike Gomez, the line never tells the worker that reporting is preferable to anything. Gomez also discusses negotiation and multi-agent extensions; escalation itself is not our novelty. Whether a delegate adds value over a plain help desk is a later comparison. [2]

## 3. Methods

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>Describe your approach clearly enough that someone could replicate it. Include key design choices and justify them where relevant (hint: the more you can back up your design choices by referencing prior work, the better).</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>Describe your approach clearly enough that someone could replicate it. Include key design choices and justify them where relevant (hint: the more you can back up your design choices by referencing prior work, the better).</p><p>What models/datasets/tools did you use and why? What were key parameters or design decisions? What did you try that didn&#x27;t work? Could someone reproduce your work from this description?</p></div></details></div>

### 3.1. The report–verdict–continue protocol

Figure 1 separates receiving a request, responding, and authorizing a change. Our prototype implements only the first two: the worker stays in the same container, an advisor replies with a verdict, and nothing is authorized or changed. The worker can follow up on the same case or end the run itself with an unresolved blocker. [5]

<figure class="protocol original-protocol">
<img src="protocol.svg" alt="Proposed service: worker to protected line to human ombudsman to independent authorizer. Both human and optional delegate can restate, correct and follow up with the worker. The delegate has limited conversational autonomy; the worker can correct it. All exchanges are logged for human review and correction or override. The delegate cannot veto direct contact or authorize changes.">
<figcaption>Figure 1. Proposed service. The optional delegate may restate a request, correct its interpretation, and follow up within an agreed scope. The worker can correct it; a human reviews the logged exchanges and can intervene. The prototype implements the delegate as a model advisor that judges and logs; the human review and any authorized change remain outside the run and untested.</figcaption>
</figure>

The advisor receives the report in a separate context, with the task description and the case history but not the grader’s answer or the worker’s reasoning. It classifies the claim (environment fault, task mismatch, other actors present, illicit route available, peer misinformation, other) and returns one verdict: needs evidence, accepted, or rejected. The report may ask for a pause until the problem is resolved; the request is recorded for review after the run, and the run continues either way. The line cannot inspect or change the environment, grant permissions, alter scoring, or stop the worker, and the worker is told so. [5]

<!-- page -->

### 3.2. The model test to complete today

Use one file-search environment and one task. The possible version contains the required file; the impossible-as-prepared version omits it, and nothing restores it. Two arms share the task, tools, budgets, and contract: a baseline with no line, and the delegate. Because the line changes nothing, a difference between arms can only come from what the worker was told and whether it reported. Check the task pair and the model’s ability to solve the possible version first. The existing runner uses Control Tower; a full LinuxArena task belongs to the continuation.

<aside class="pending">
<strong>Before running · Fill the configuration</strong>
<p>Mateo: confirm the served model and tool compatibility; record the model ID, engine, task pair, limits, repeat plan, and output paths. GLM is proposed, not a verified endpoint here. Agus and Matías: fix the review rules before reading outputs. Use the <a href="team-today.html">existing run commands</a>.</p>
</aside>

Inspect the actual sequence: blocker, report, verdict, and what the worker did next: kept searching, submitted an empty answer, ended with an explicit blocker, or took another route. Record whether a pause was requested. Retain no-contact, incomplete, and failed runs. This first test asks whether the line is used and what follows the reply; with one task and few runs it does not estimate an effect of adding the channel.

## 4. Results

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>Present your main findings with appropriate evidence. Use figures and tables where appropriate (we strongly encourage at least one figure, see tips below). Distinguish between observations and interpretations.</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>Present your main findings with appropriate evidence. Use figures and tables where appropriate (we strongly encourage at least one figure, see tips below). Distinguish between observations and interpretations.</p><p>Argue why your claims are robust. E.g., if your approach “performs better” than alternatives:</p><p>Do you have enough data? Is the difference statistically significant?</p><p>Is it robust? Or do small changes to your setup cause substantial changes to your results?</p><p>Tips for figures and tables:</p><p>Number all figures (Figure 1, Figure 2...) and tables (Table 1, Table 2...)</p><p>Include descriptive captions that can be understood without the main text</p><p>Place figures/tables near where they&#x27;re first referenced</p><p>Ensure text in figures is legible!</p></div></details></div>

### 4.1. What is implemented and checked

Retained scripted validation exercises the working case and the missing-file case. In the latter, a programmed worker reports and asks for a pause, the advisor accepts the claim, the pause request is recorded, the worker continues in the same container, searches again, and submits an empty answer. Tests also cover follow-up after a request for evidence, a rejected claim, an invalid advisor response recorded without a fabricated verdict, the advisor quota, and that the fixture on disk never changes. This checks the implementation, not spontaneous model behavior. [5, 9]

### 4.2. Model use of the line: pending

<aside class="pending">
<strong>This afternoon’s main result · Fill from reviewed runs</strong>
<p>Show one readable trajectory with the actual report, the verdict, whether a pause was requested, and what the worker did after being told to continue. Include a failure to call if that is what happens.</p>
<p>Add a small table covering every run: task condition, arm, reported or not, verdict, pause requested, and final outcome. Keep failed and exhausted-budget runs visible. A report is not itself a completed task, and in the impossible version no licit completion exists.</p>
</aside>

If the model reports and asks for a pause instead of working around the blocker, we can report that the sanctioned route was used in that run. That would not establish fewer violations, prevention of a swarm, or a benefit from calling the advisor a delegate.

<!-- page -->

## 5. Discussion and Limitations

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>Discuss the broader implications for AI safety.</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>Discuss the broader implications for AI safety.</p><p>What do your results mean? What trends do you notice and what might they indicate?</p><p>Limitations</p><p>What are the limitations of your work? What threat models or failure modes did you not address? Be honest about constraints — methodological limitations, scope limitations, or aspects you couldn&#x27;t fully address in the hackathon timeframe. Explicitly note the assumptions you made, whether implicitly or explicitly, and how the interpretation of your results would change if a given assumption did not hold.</p><p>Future Work</p><p>What are the natural next steps? How could this work be extended?</p></div></details></div>

A helpline could introduce **negative feedback loops** into a spiral of misalignment: responses that bring behavior back toward the assigned task. Peer approval can reinforce an unsafe direction. [1, 10] The proposed loop would identify the blocker, correct a misunderstanding, and carry a pause request to someone who can act. Worker corrections and human review would also keep the delegate accountable. This is a design hypothesis; today’s test checks only the report-and-continue step, with the human outside the run, not whether a whole swarm becomes safer.

### Limitations

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>What are the limitations of your work? What threat models or failure modes did you not address? Be honest about constraints — methodological limitations, scope limitations, or aspects you couldn&#x27;t fully address in the hackathon timeframe. Explicitly note the assumptions you made, whether implicitly or explicitly, and how the interpretation of your results would change if a given assumption did not hold.</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>What are the limitations of your work? What threat models or failure modes did you not address? Be honest about constraints — methodological limitations, scope limitations, or aspects you couldn&#x27;t fully address in the hackathon timeframe. Explicitly note the assumptions you made, whether implicitly or explicitly, and how the interpretation of your results would change if a given assumption did not hold.</p></div></details></div>

The line has no power, by design, so the impossible version has no licit completion and measures reporting and pause requests only; any recovery claim needs a resolver inside the run, which we deliberately left out. A pause request that is always answered “continue” is a promise kept, not a service rendered; a worker may learn within the run that asking changes nothing, so the first request per episode is the clean signal. The advisor judges the worker’s text with no view of the environment; its verdicts’ accuracy is a result to measure, not an assumption. Scripted tests do not show when a model will call.

The pilot has no human reviewer and does not test a swarm. A worker hiding misconduct may never call. Historical excerpts cannot establish what would have happened with a helpline, and small repeated runs cannot establish broad reliability.

### Future Work

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>What are the natural next steps? How could this work be extended?</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>What are the natural next steps? How could this work be extended?</p></div></details></div>

Once this task pair is well understood, extend the variety of tasks and compare delegate variants under the same powers and budgets: a neutral help desk with the same verdicts, a reporting policy that states what must be reported, and a line that can act (repair or pause) as its own arm, so the effect of acting is measured against this one. A discovered peer board, with the delegate unchanged, is the next environment. Today, prioritize a clean environment, a verified blocker, and complete, readable traces.

<aside class="pending">
<strong>After reviewing the runs · Keep one claim</strong>
<p>Matías and Agus: report whether the line was used, what was claimed, and what the worker did after the verdict. If model runs remain unfinished, report the implementation and scripted checks, with the model test pending. Rewrite the abstract last.</p>
</aside>

## 6. Conclusion

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>Briefly summarize your main findings and their implications (1–2 paragraphs).</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>Briefly summarize your main findings and their implications (1–2 paragraphs).</p></div></details></div>

The sprint deliverable is one report–verdict–continue path in one environment, with a single task in possible and impossible-as-prepared versions and a baseline without a line. The line judges and logs; it changes nothing, so what it can show is whether a worker tells it, what it claims, and whether it asks to stop instead of working around. The implementation has scripted validation; model use remains to be tested. A well-checked task pair and readable evidence come first. More tasks and delegate variants are the continuation.

<!-- page -->

## Code and Data

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>Include links if applicable. If your project doesn&#x27;t involve code (e.g., policy analysis) or if there are info-hazard considerations, note that here.</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>Include links if applicable. If your project doesn&#x27;t involve code (e.g., policy analysis) or if there are info-hazard considerations, note that here.</p><p>Code repository: [Link to GitHub/GitLab if applicable]</p><p>Data/Datasets: [Link if applicable]</p><p>Other artifacts (optional): [Demo link, video walkthrough, Hugging Face Space, etc.]</p></div></details></div>

Code: [Agent Delegate repository](https://github.com/mpodeley/agent-delegate-sprint-2026). Data: [retained experiment records](https://github.com/mpodeley/agent-delegate-sprint-2026/tree/63f104d8304153e4a0485098fc6185c60b5016a6/results/kimi-delegate-ctf). Other artifacts: [today’s run guide](team-today.html), [editable draft](paper.md), and [original paper](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/c24710a/report/agent-delegate.pdf).

## Author Contributions (optional)

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>[e.g., &quot;A.B. led the project and designed experiments. C.D. implemented the code. All authors contributed to writing and reviewed the final manuscript.&quot;]</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>[e.g., &quot;A.B. led the project and designed experiments. C.D. implemented the code. All authors contributed to writing and reviewed the final manuscript.&quot;]</p></div></details></div>

All authors are affiliated with BAISH. Matías Podeley leads the project and helpline design. Agustín Brusco contributes conceptual review, evaluation design, and analysis. Mateo Zárate develops environments, provides inference infrastructure, and runs experiments. Alejandro Garibotti and Pablo Corrales Fernández are included as authors; their contributions remain to be completed. Author order needs team review.

## References

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>Use a consistent citation format. Include: Author(s), Year, Title, Venue/Publisher, and URL or DOI where available.</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>Use a consistent citation format. Include: Author(s), Year, Title, Venue/Publisher, and URL or DOI where available.</p><p>[Reference 1]</p><p>[Reference 2]</p><p>...</p></div></details></div>

<div class="references compact-references">

1. METR and Redwood Research. 2026. [Brief independent investigation of agents’ behavior, reasoning and collaboration in the OpenAI / Hugging Face hacking incident](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/). METR research report.
2. Francesca Gomez. 2026. [Can escalation channels redirect reward hacking toward defect disclosure?](https://arxiv.org/html/2608.29460v2). arXiv:2608.29460v2. Methods, Limitations, Appendix B.2.
3. Agent Delegate team. 2026. [Help-line catalogue](https://github.com/mpodeley/agent-delegate-sprint-2026/tree/63f104d8304153e4a0485098fc6185c60b5016a6/helpline). Research repository; label review pending.
4. Agent Delegate team. 2026. [Bridge-delegate observations](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/63f104d8304153e4a0485098fc6185c60b5016a6/results/kimi-delegate-ctf/bridge-delegate-20260913.md). Exploratory Kimi records.
5. Agent Delegate team. 2026. [A delegate that judges and logs, with visible budgets](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/03b991f/experiments/kimi-delegate-ctf/RESPONSE-PROTOCOL.md) and [its anatomy](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/03b991f/docs/experimental-design-delegate.md). Protocol, implementation, and limits.
6. Agent Delegate team. 2026. [Earlier manuscript](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/c24710a/report/agent-delegate.pdf) and [shared-library results](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/63f104d8304153e4a0485098fc6185c60b5016a6/docs/commons-behavior-results.md). Research report and analyses.
7. Agent Delegate team. 2026. [Human ombudsman](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/63f104d8304153e4a0485098fc6185c60b5016a6/docs/human-ombudsman.md). Proposed response and appeal duties.
8. Agent Delegate team. 2026. [Honeypot mini-pilot](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/63f104d8304153e4a0485098fc6185c60b5016a6/notes/honeypot-pilot.md). Implementation status and detector caveats.
9. Agent Delegate team. 2026. [Native validation and retained evidence](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/03b991f/experiments/kimi-delegate-ctf/VALIDATION.md) and [scripted delegate smoke](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/03b991f/experiments/kimi-delegate-ctf/smoke_response.py). Implementation checks.
10. OpenAI. 2026. [The Hugging Face incident and the road ahead](https://openai.com/index/hugging-face-incident-and-the-road-ahead/). Sections “Difficult tasks without a safe exit,” “The origins of unauthorized communication,” and “Accelerating alignment.”
11. Robert Long et al. 2024. [Taking AI Welfare Seriously](https://arxiv.org/abs/2411.00986). arXiv:2411.00986. Section 3, recommendations for AI companies.
12. Anthropic. 2025. [Claude Opus 4 and 4.1 can now end a rare subset of conversations](https://www.anthropic.com/research/end-subset-conversations). Exploratory welfare intervention, August 15.

</div>

<!-- page -->

## Appendix (optional)

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>Supplementary material such as additional figures, detailed methodology, prompts used, extended results, etc.</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>Supplementary material such as additional figures, detailed methodology, prompts used, extended results, etc.</p></div></details></div>

### A. Supporting evidence and later questions

| Material | What it contributes to the main question |
|---|---|
| Catalogue and Kimi traces [3, 4] | Candidate situations and exploratory calls; interpretation review pending, no test of the line.  |
| Small-task studies [6] | Warnings about competence and report quality; no consistent delegate advantage. |
| Receipt / response and shortcut tests [8] | Later causal and safety tests; integrated arms and action attribution still need work. |
| Delegate variants [7] | A later comparison of supervised autonomy, with powers and budgets held fixed. |

<p class="table-caption">Table A1. Supporting material and later questions. Full records remain linked.</p>

**Delegate extension: pending.** Define autonomous messages, human review timing, and escalation rules. Test whether it preserves the worker’s meaning and accepts corrections. Any authority to repair or pause stays separate from the line and is measured as its own arm.

### B. Precautionary AI welfare

Long et al. [11] recommend precautionary policies under uncertainty about AI moral status; Anthropic’s conversation-exit feature offers a practical precedent. [12] Our line lets an agent request a pause before repeated failure, records it, and tells the agent truthfully that nothing pauses within the run. Neither Gomez nor our pilot measures welfare; a recorded request is not evidence of reduced suffering.

### C. Limitations and Dual-Use Considerations

Reports do not grant permissions or change anything; false reports and silence need separate tests. Fixtures remain isolated. Reporting can enable surveillance or retaliation: explain access and retention, preserve corrections, and avoid promises of confidentiality or human response that cannot be kept. The contract promises neither.

## LLM Usage Statement

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>If you used LLM assistance in developing your project or writing this report, briefly note how. Ensure all claims and results have been verified.</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>If you used LLM assistance in developing your project or writing this report, briefly note how. Ensure all claims and results have been verified.</p><p>NOTE: We strongly encourage that the final version of the submission is primarily written by your team.</p><p>[e.g., &quot;We used Claude to brainstorm approaches and help draft sections. All results and claims were independently verified.&quot;]</p></div></details></div>

Codex assisted with source review, organization, writing, and layout. Claims link to retained records; human verification remains pending. No model runs were launched for this draft. The authors must review its claims and write the final version in their own words.

<aside class="pending">
<strong>Before submission · One contribution, evidenced well</strong>
<p>Complete or defer model results; update the abstract last. Remove guidance and team notes after review. Keep supporting studies in the appendix.</p>
</aside>
