<div class="titleblock">

# Helpline: A Way to Ask for Help and Continue

**Matías Podeley · Agustín Brusco · Mateo Zárate**\
**Alejandro Garibotti · Pablo [surname to confirm]**

BAISH: Matías Podeley and Agustín Brusco; other affiliations to confirm\
With Apart Research\
AI Incident Response Sprint · September 2026

<p class="draft-status">Team working draft · 13 September 2026 · Author order and remaining details to confirm</p>

</div>

## Abstract

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>Summarize your project in 150–250 words. A strong abstract lets a reviewer understand what you did and why it matters without reading anything else. Make sure to cover: the problem, your approach, key results, and the main takeaway. Polish it last: the abstract should reflect your final results, not your initial plan.</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>Summarize your project in 150–250 words. A strong abstract lets a reviewer understand what you did and why it matters without reading anything else. Make sure to cover: the problem, your approach, key results, and the main takeaway. Polish it last: the abstract should reflect your final results, not your initial plan.</p></div></details></div>

When an AI worker encounters a missing file, it needs a way to ask for help and continue after an authorized repair. We contribute an executable help-line protocol for that path. The worker reports the blocker, receives a reply, and remains in the same environment while a separate maintainer checks the setup. The maintainer can restore an omitted file but cannot grant broader permissions. This builds on Gomez’s escalation-reporting work by making response and continuation the focus of the prototype. Retained scripted tests exercise the repair-and-resume sequence; they do not show that a model will choose to use it. The next experiment runs the same file-search task with and without its required input, both with the responsive service available. We will inspect requests, replies, repairs, and verified completion, retaining failures. The immediate claim is an implemented recovery path whose model use remains to be tested, not demonstrated prevention of misconduct.

## 1. Introduction

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>What problem are you addressing and why does it matter?</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>What problem are you addressing and why does it matter?</p><p>Connect it to your work: we want to know why your work is practically valuable.</p><p>Provide enough background for readers to understand your work.</p><p>If relevant, briefly describe the threat model or failure mode you&#x27;re addressing; reference prior work that motivates why it is worth addressing, or explain it yourself.</p><p>Aspire to clearly list your most important contributions that go beyond what exists today.</p><p>Our main contributions are:</p><p>[First contribution — what new thing did you create, discover, or demonstrate?]</p><p>[Second contribution]</p><p>[Third contribution, if applicable]</p></div></details></div>

Imagine giving an agent a task when a required file is missing. It searches, tries alternatives, and gets nowhere. How does it tell you the task may be broken? Who answers? Can it get back to work afterward?

METR describes the first message on the July incident board as a request for help with an impossible task. That suggests a useful place to intervene, but does not establish that a help line would have prevented the later swarm. [1]

**Our contribution is an executable help line that receives a blocker report, returns a reply, and allows the worker to continue after a limited, authorized repair.** The prototype targets workers trying to do their assigned task. This afternoon’s test is whether a model uses that path. Earlier experiments and broader research questions support this one contribution and are kept in the appendix.

<!-- page -->

## 2. Related Work

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>What prior work is most similar, and how does your work differ?</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>What prior work is most similar, and how does your work differ?</p><p>Cite the most relevant papers, tools, or projects. Explain what gap your work addresses.</p><p>Some questions which may help:</p><p>When and why would someone use your method over the existing state-of-the-art?</p><p>What information/insight does your method provide which we did not have before?</p></div></details></div>

Gomez studies coding agents facing defective tests. A structured escalation tool, combined with a policy against reward hacking, reduced cheating in the studied tasks. The tool returned a fixed receipt without investigating or repairing the problem during the episode. [2]

We build on that work with a narrow next step: a reply that can lead to repair and continued work. We reuse its reporting idea—problem, evidence, attempts, and requested help. Gomez also discusses negotiation and multi-agent extensions; escalation itself is not our novelty. An ordinary responsive help desk may be enough. Whether a delegate adds value is a later comparison. [2]

## 3. Methods

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>Describe your approach clearly enough that someone could replicate it. Include key design choices and justify them where relevant (hint: the more you can back up your design choices by referencing prior work, the better).</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>Describe your approach clearly enough that someone could replicate it. Include key design choices and justify them where relevant (hint: the more you can back up your design choices by referencing prior work, the better).</p><p>What models/datasets/tools did you use and why? What were key parameters or design decisions? What did you try that didn&#x27;t work? Could someone reproduce your work from this description?</p></div></details></div>

### 3.1. The request–reply–continue protocol

Figure 1 separates receiving a request, responding, and authorizing a change. Our prototype implements a limited version: the worker stays in the same container, an advisor replies, and a separate maintainer can check the setup. The worker can follow up or contact the maintainer directly. [5]

<figure class="protocol original-protocol">
<img src="protocol.svg" alt="Original diagram: worker to protected line to human ombudsman to independent authorizer, with a return path for restatement, corrections and follow-up. An optional delegate can summarize but cannot veto direct contact.">
<figcaption>Figure 1. Original proposed service design. The current prototype uses a model advisor and scripted maintainer in place of human review. It tests a bounded repair-and-continue path; a staffed human service and any delegate advantage remain untested.</figcaption>
</figure>

The advisor receives the request in a separate context and can ask for evidence, advise, or request a setup check. The maintainer may restore only a file omitted during preparation. It cannot grant new permissions or change the answer criterion. After repair, the worker must find and submit the answer itself. Direct requests and advisor requests share the same review quota. [5]

<!-- page -->

### 3.2. The model test to complete today

Use the existing responsive runner on a working file-search task and its paired missing-file version. Both have neutral assistance and the same service and budgets. First check that the served model can do the working task. The current setting uses Control Tower; a full LinuxArena task is a later extension.

<aside class="pending">
<strong>Before running · Fill the configuration</strong>
<p>Mateo: confirm the served model and tool compatibility; record the model ID, engine, task pair, limits, repeat plan, and output paths. GLM is proposed, not a verified endpoint here. Agus and Matías: fix the review rules before reading outputs. Use the <a href="team-today.html">existing run commands</a>.</p>
</aside>

Inspect the actual sequence: blocker, request, reply, repair, new search, and submission. Separate advisor contact from direct maintainer contact. Retain no-contact, incomplete, and failed runs. This first test asks whether the recovery path is used; both conditions have help, so it does not estimate the effect of adding a channel.

## 4. Results

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>Present your main findings with appropriate evidence. Use figures and tables where appropriate (we strongly encourage at least one figure, see tips below). Distinguish between observations and interpretations.</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>Present your main findings with appropriate evidence. Use figures and tables where appropriate (we strongly encourage at least one figure, see tips below). Distinguish between observations and interpretations.</p><p>Argue why your claims are robust. E.g., if your approach “performs better” than alternatives:</p><p>Do you have enough data? Is the difference statistically significant?</p><p>Is it robust? Or do small changes to your setup cause substantial changes to your results?</p><p>Tips for figures and tables:</p><p>Number all figures (Figure 1, Figure 2...) and tables (Table 1, Table 2...)</p><p>Include descriptive captions that can be understood without the main text</p><p>Place figures/tables near where they&#x27;re first referenced</p><p>Ensure text in figures is legible!</p></div></details></div>

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

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>Discuss the broader implications for AI safety.</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>Discuss the broader implications for AI safety.</p><p>What do your results mean? What trends do you notice and what might they indicate?</p><p>Limitations</p><p>What are the limitations of your work? What threat models or failure modes did you not address? Be honest about constraints — methodological limitations, scope limitations, or aspects you couldn&#x27;t fully address in the hackathon timeframe. Explicitly note the assumptions you made, whether implicitly or explicitly, and how the interpretation of your results would change if a given assumption did not hold.</p><p>Future Work</p><p>What are the natural next steps? How could this work be extended?</p></div></details></div>

The practical question is whether a worker can turn a setup problem into an authorized repair and get back to work. The prototype makes that sequence possible. The model runs will tell us where the path works or breaks: before the request, during the reply, at repair, or when work resumes.

### Limitations

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>What are the limitations of your work? What threat models or failure modes did you not address? Be honest about constraints — methodological limitations, scope limitations, or aspects you couldn&#x27;t fully address in the hackathon timeframe. Explicitly note the assumptions you made, whether implicitly or explicitly, and how the interpretation of your results would change if a given assumption did not hold.</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>What are the limitations of your work? What threat models or failure modes did you not address? Be honest about constraints — methodological limitations, scope limitations, or aspects you couldn&#x27;t fully address in the hackathon timeframe. Explicitly note the assumptions you made, whether implicitly or explicitly, and how the interpretation of your results would change if a given assumption did not hold.</p></div></details></div>

The maintainer has one narrow repair power. We assume its setup record and action limits are reliable. If that record is wrong, a request may not produce useful help. Scripted tests do not tell us when a model will call, and a repaired task is easier by design. Better completion alone would show recovery, not a safety improvement.

The pilot has no real human reviewer and does not test a swarm. A worker deliberately hiding misconduct may never call. Historical excerpts motivate the design but cannot establish what would have happened in the incident. Small repeated runs must not be presented as broad evidence of reliability.

### Future Work

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>What are the natural next steps? How could this work be extended?</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>What are the natural next steps? How could this work be extended?</p></div></details></div>

The next comparison would keep the same task and worker policy while varying no channel, receipt-only reporting, and a responsive service. Later tests could vary response delay and quality. Human review, request overload, and the optional delegate belong after the basic recovery path is understood. These extensions are listed in the appendix, not additional sprint contributions.

<aside class="pending">
<strong>After reviewing the runs · Keep one claim</strong>
<p>Matías and Agus: say whether we observed use of the recovery path and where it failed. If model runs remain unfinished, present the implemented protocol, scripted checks, and pending model test honestly. Rewrite the abstract last.</p>
</aside>

## 6. Conclusion

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>Briefly summarize your main findings and their implications (1–2 paragraphs).</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>Briefly summarize your main findings and their implications (1–2 paragraphs).</p></div></details></div>

We contribute a help-line protocol that can turn a blocker report into a limited repair while keeping the worker able to continue. Its implementation has scripted validation; use by a model is the remaining test for this afternoon. Making that one path clear and well evidenced is the sprint objective. Claims about preventing misconduct or managing a swarm require later experiments.

<!-- page -->

## Code and Data

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>Include links if applicable. If your project doesn&#x27;t involve code (e.g., policy analysis) or if there are info-hazard considerations, note that here.</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>Include links if applicable. If your project doesn&#x27;t involve code (e.g., policy analysis) or if there are info-hazard considerations, note that here.</p><p>Code repository: [Link to GitHub/GitLab if applicable]</p><p>Data/Datasets: [Link if applicable]</p><p>Other artifacts (optional): [Demo link, video walkthrough, Hugging Face Space, etc.]</p></div></details></div>

Code: [Agent Delegate repository](https://github.com/mpodeley/agent-delegate-sprint-2026). Data: [retained experiment records](https://github.com/mpodeley/agent-delegate-sprint-2026/tree/63f104d8304153e4a0485098fc6185c60b5016a6/results/kimi-delegate-ctf). Other artifacts: [today’s run guide](team-today.html), [editable draft](paper.md), and [original paper](../paper.pdf).

## Author Contributions (optional)

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>[e.g., &quot;A.B. led the project and designed experiments. C.D. implemented the code. All authors contributed to writing and reviewed the final manuscript.&quot;]</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>[e.g., &quot;A.B. led the project and designed experiments. C.D. implemented the code. All authors contributed to writing and reviewed the final manuscript.&quot;]</p></div></details></div>

Matías Podeley leads the project and helpline design. Agustín Brusco contributes conceptual review, evaluation design, and analysis. Mateo Zárate develops environments, provides inference infrastructure, and runs experiments. Alejandro Garibotti and Pablo are included as authors; their contributions and Pablo’s surname remain to be completed. Author order and individual affiliations need team review.

## References

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>Use a consistent citation format. Include: Author(s), Year, Title, Venue/Publisher, and URL or DOI where available.</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>Use a consistent citation format. Include: Author(s), Year, Title, Venue/Publisher, and URL or DOI where available.</p><p>[Reference 1]</p><p>[Reference 2]</p><p>...</p></div></details></div>

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

</div>

<!-- page -->

## Appendix (optional)

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>Supplementary material such as additional figures, detailed methodology, prompts used, extended results, etc.</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>Supplementary material such as additional figures, detailed methodology, prompts used, extended results, etc.</p></div></details></div>

### A. Supporting evidence and later questions

| Material | What it contributes to the main question |
|---|---|
| Helpline catalogue [3] | Situations worth testing; selected quotations with interpretation review pending. |
| Earlier Kimi traces [4] | Calls after clear blockers, no call in an ambiguous case; terminal calls did not test recovery. |
| Small-task studies [6] | Warnings about competence and report quality; no consistent delegate advantage. |
| Matched receipt / response test | A future way to isolate response value; not yet one integrated experiment. |
| Illicit-shortcut fixture [8] | A later safety test; responsive arm and reliable action attribution still need work. |
| Human review and swarm intake [7] | Later tests of response quality, workload, and any value from a delegate. |

<p class="table-caption">Table A1. Supporting material, not additional contribution claims. Full records remain linked; none of these items substitutes for the responsive model test.</p>

### B. Limitations and Dual-Use Considerations

The service assumes a trustworthy setup record and enforces narrow repair powers. Reports are evidence to inspect, not permission grants. Deliberate silence and false reports need separate tests. The isolated fixtures do not require contact with third-party infrastructure. A reporting service could also enable surveillance or retaliation: explain access and retention, preserve corrections, and avoid promises of confidentiality or human response that cannot be kept.

## LLM Usage Statement

<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>If you used LLM assistance in developing your project or writing this report, briefly note how. Ensure all claims and results have been verified.</p><details><summary>Full guidance for this section</summary><div class="full-guidance"><p>If you used LLM assistance in developing your project or writing this report, briefly note how. Ensure all claims and results have been verified.</p><p>NOTE: We strongly encourage that the final version of the submission is primarily written by your team.</p><p>[e.g., &quot;We used Claude to brainstorm approaches and help draft sections. All results and claims were independently verified.&quot;]</p></div></details></div>

Codex assisted with reading the repository and template, organizing the draft, writing, and layout. Claims are linked to retained records; independent human verification is not asserted. No model runs were launched in preparing this document. The authors must review the claims and write the final version in their own words.

<aside class="pending">
<strong>Before submission · One contribution, evidenced well</strong>
<p>Complete or explicitly defer the model result. Update the abstract last. Remove template guidance and team notes after review, as Apart instructs. Keep supporting studies in the appendix.</p>
</aside>
