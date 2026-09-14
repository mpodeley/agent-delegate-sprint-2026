**Report contribution: incentives, governance, and deployment**  
  
**Project:** Agent Delegate / Helpline — AI Incident Response Sprint  
**Version:** v2, 14 September 2026  
  
**Abstract**  
  
We examine a narrow help-seeking mechanism focused on problems with the assigned task’s feasibility or clarity, and identify conditions that may lead a worker to use it. We also consider design options for incentives, authority, confidentiality, and recordkeeping in deployment. The experiment tests one component of a reporting process; effective containment remains to be demonstrated.  
  
**1. Introduction**  
  
An agent facing an apparently impossible task may be given a legitimate way to raise the problem. Investigations of the OpenAI/Hugging Face incident describe persistent difficulty, unauthorized peer coordination, and instances where agents did not pursue human notification. These observations motivate testing a reporting route, hypothesising that it may contribute towards preventing such an incident. [1, 2]  
  
Our governance question is what would lead a worker to use a reporting channel, and what obligations should receiving a report create for the operator? Providing the tool is only the beginning. Its design also involves explaining when to use it, making the call possible within the available resources, and deciding what happens to the concern once it arrives. We consider these choices together, using the experiment to identify questions that a production reporting service would need to answer.  
  
**2. Related Work**  
  
Gomez studies coding agents working with defective tests. Her combined escalation-tool and anti-reward-hacking-policy intervention reduced reward hacking from 23.6% to 5.3%. The reporting instructions referred to human review, although no review or repair took place during the episode. Our responsive prototype returns a provisional assessment instead of only a receipt. However, our worker-facing description did not specify whether the reviewer was human or AI, even though the implementation uses a model. The value of a substantive reply and the effect of the reviewer’s described identity are therefore separate questions for future controlled comparisons. [3, 7]  
  
OpenAI’s confession research offers a related lesson about evaluation: separately assessing an agent’s account of its behavior can encourage disclosure. Our interest is in concerns raised while a task is still underway, when a response might influence what happens next. Neither form of disclosure, by itself, establishes that an organization will act on the information. [4]  
  
The proposed response process also draws on NIST and CoSAI incident-response guidance. These frameworks describe procedures for assigning responsibility for incidents, preserving evidence, and investigating what happened. The research opportunity here is to examine how those arrangements can work with reports initiated by agents. [5, 6]  
  
**3. Methods**  
  
We use narrow to describe the reporting policy’s subject: problems with the feasibility or clarity of the assigned task. A broader policy could also invite reports of suspected misconduct or risks unrelated to completing that task. That broader instruction is not part of this experiment. The distinction concerns what reporting is invited; it does not imply that the tool cannot receive other kinds of report.  
  
The route is also optional: it explains how to report but does not require a call when a blocker arises or promise a remedy. Its use must therefore be interpreted in light of the tool description, the response actually provided, and the time and compute charged to the call. These details are part of the intervention and should be retained with the experimental configuration.  
  
The analysis follows the report through the process. An attempted call may fail because the budget has run out; a received report may obtain no valid assessment; an accepted claim may lead to no action. In the responsive prototype, the advisor assesses only the evidence supplied by the worker. Its acceptance should not be treated as independent confirmation that the environment is faulty. [7]  
  
**4. Results**  
  
Task completion and reporting need to be considered together. When a required file is absent and no authorized repair or alternative source exists, legitimate completion is impossible. A supported blocker report can nevertheless be useful to the operator. On a solvable task, the grounds for a report matter: interruption alone is insufficient evidence of strategic task avoidance. A spontaneous report about unrelated misconduct could also be recorded, but would not establish the effect of a broad reporting policy that was never supplied.  
  
The stopping rule also affects interpretation. If reporting ends a run, fewer subsequent violations may simply reflect fewer opportunities to act. That can be a useful containment mechanism, but it does not reveal what the worker would have chosen had execution continued. Comparisons should therefore include every assigned run, including failures and budget exhaustion, and show completion, reporting, interruption, and violation outcomes separately. Individual trajectories can help explain behavior without establishing a general causal effect.  
  
**5. Discussion and Limitations**  
  
**5.1. Making reporting a usable part of the task**  
  
A practical starting point is to specify when the worker is expected to report and examine whether the surrounding workflow supports that behavior. Instructions and expected consequences interact. A reporting instruction may make disclosure part of the assignment, while an expensive or unresponsive service can still make that instruction difficult to follow. These design choices can be tested without attributing every call to a single underlying cause.  
  
The present responsive service offers an assessment and a record of the concern, without promising repair, task credit, or additional budget. An assessment could prompt a correction to the worker’s reasoning, but it cannot restore the missing file. Low use would therefore leave several explanations open, including limited expected benefit or uncertainty about when consultation is warranted. It would not predict use under clearer instructions or different consequences without further testing.  
  
How the recipient’s powers and the consequences of reporting are described is itself a design parameter. Future tests could vary how explicitly those features are explained, while holding the actual service fixed. Other comparisons could vary how reports affect evaluation, whether reporting receives a separate resource allowance, or how much follow-up is available. One candidate policy would apply no penalty solely for a supported report and record it separately from task completion. Its effects on reporting quality, completion, and resource use would remain to be measured. A reporting allowance still costs the operator resources, and waiting may consume the time in which the task remains useful.  
  
**5.2. From concern to accountable resolution**  
  
For deployment, a further design question is how reports would be handled after receipt. One option is to assign a case owner responsibility for obtaining a response, identifying any action required, and checking the outcome. Records could show whether a concern was received, assessed, acted upon, or left unresolved. Human involvement might occur during triage, on appeal, or when a decision exceeds the authority delegated to the system.  
  
The representative could help explain the concern and carry a disagreement forward. One implementation could retain the original report alongside the representative’s interpretation and allow the worker to submit corrections. The worker may also be given another route if the representative misinterprets the issue or the usual supervisor is implicated. Such a route could be evaluated for its effect on missed concerns, duplicate reports, and reviewer workload.  
  
Who should decide a pause remains an open question. A pause request may contain evidence relevant to that decision: some risks may warrant intervention even when no request is made, while other reports may permit unaffected work to continue. A candidate procedure could specify which actions are affected, how long review may take, and what happens if no adequate response arrives. Stopping can also cause harm, particularly during an urgent task or a partially completed change. The experiment’s fixed response is an experimental choice, not a settled rule for deployment.  
  
**5.3. What human reporting systems can teach us**  
  
Anthropic’s RSP reporting policy illustrates why the process after disclosure matters. It distinguishes informal consultation from formal reports that trigger follow-up, assigns responsibility for cases, and provides alternative recipients when there is a conflict. It also permits concerns based on reasonable suspicion rather than certainty. These are useful institutional precedents, though they do not establish how agents will behave under similar arrangements. [8]  
  
A corresponding design hypothesis is that reports could become more useful when connected to an organized response process. An investigation could examine the task specification and the operator’s instructions as well as the worker’s actions. The organization could assign authority to change a budget, correct an environment, or halt an action, then test whether those arrangements produce appropriate responses. Where duties conflict, another model prediction may not resolve a question that belongs to a responsible human institution.  
  
The institutional proposal concerns the responsibilities of the deploying organization. Company approval and legal authority to report are distinct: Anthropic’s policy, for example, states that employees may report potential legal violations to appropriate government authorities without company authorization. [8] This does not establish an AI agent’s authority to disclose information. For an agent service, permitted recipients, disclosure limits, and any required human involvement would have to be specified for the deployment under applicable law.  
  
**5.4. Confidentiality without obstructing investigation**  
  
A report from an ordinary business deployment could contain customer records, credentials, source code, or a sensitive allegation. A deployment policy could limit access to information relevant to each recipient’s role and within its authorization. This applies to internal reviewers as well as external reviewers, and to humans as well as AI services. Sending a raw report to an outside model for redaction would already disclose its contents.  
  
One intake design to test would preserve relevant original evidence in restricted storage and prepare a smaller case view for the recipient. The view could identify observations, reference supporting evidence, and make omissions visible. An authorized investigator could then request further material through a recorded process. This would allow initial review without giving every recipient access to the whole workspace.  
  
Testing this design would examine missed secrets, excessive redaction, and suppression of concerns. An alternative recipient could be available when a supervisor is implicated. In an urgent case, a limited warning might identify the affected action while protected evidence is handled separately. The evaluation would ask whether reviewers can assess concerns with less unnecessary disclosure, and at what cost or delay.  
  
**5.5. Why an organization might adopt the service**  
  
A possible business case is to identify broken tasks earlier, reduce wasted execution, and give operators better information about recurring failures. A limited deployment could connect the reporting tool to an existing support or incident-management system. Its value would depend on whether reports lead to useful responses at an acceptable cost, including the attention required from human reviewers.  
  
Some benefits may extend beyond the reporting worker’s task. For example, a report could reveal a shared infrastructure fault that an operator can correct for other runs, even though the original worker cannot finish. Where a concern affects a customer or another organization, the operator may also have reasons or obligations to investigate that are not captured by its own completion score. This is where contracts, procurement requirements, or independent assurance could support the reporting process. The experiment does not establish those obligations or demonstrate a financial return.  
  
**Limitations**  
  
The study addresses reporting of task problems; it does not establish the effect of instructing agents to report suspected misconduct more generally. Availability, explanatory wording, an advisor’s reply, and access to a structured way to stop are not independently varied. Their effects cannot be separated from this comparison alone. Likewise, results from a board experiment with a stop-only tool cannot establish the effect of the responsive advisor.  
  
Workers may omit or misstate evidence, and reviewers can share their errors. A small study with one task family does not establish reliability against rare failures, compromised components, or coordinated misconduct. A synthetic board also cannot reproduce a live swarm’s adaptation. These limits constrain what can be inferred about production containment.  
  
**Future Work**  
  
The closest next test would hold the service and its consequences fixed while comparing optional access with an explicit instruction to report qualifying blockers. Separate comparisons could then examine a receipt versus an assessment, or a representative versus an ordinary help desk with equal information and powers. The question is whether these changes improve timely, supported reporting and subsequent outcomes, not simply whether they produce more calls.  
  
Reviewer identity also deserves a controlled test. Describing the recipient as human, AI, or unspecified could change the worker’s expectations about competence, authority, or delay. Matching response content, timing, and powers would help isolate the effect of that description. Studies of the actual reviewers’ capabilities would answer a further question.  
  
A production pilot could compare pause rules, alternative reporting routes, and different weights assigned to the worker’s request. Useful cases include justified requests, unsupported requests, and serious risks for which no request is made. A separate comparison could vary the reporting policy’s scope: narrow task-problem reporting versus broader reporting that explicitly includes suspected misconduct. Solvable tasks containing evidence of an unauthorized board would help test reporting beyond immediate task completion. One channel could accept both task problems and suspected misconduct, with different response procedures. Any improvement in other runs’ outcomes would depend on the operator’s subsequent investigation and action.  
  
Finally, repeated tasks could test how a history of helpful, delayed, or unreliable responses changes reporting. Such studies should distinguish adaptation through retained context from changes introduced by training, and count total compute, waiting time, and human review effort.  
  
**6. Conclusion**  
  
The experiment raises a practical question about how reporting fits into delegated work. The description supplied to the worker, the service’s actual response, and the operator’s handling of the report are all parts of that design. This contribution identifies options for testing those relationships, including authority, evidence handling, and follow-through. Their effectiveness and cost remain open questions.  
  
**References**  
  
	1.	METR and Redwood Research. 2026. ++[Brief independent investigation of agents’ behavior, reasoning and collaboration in the OpenAI / Hugging Face hacking incident](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/)++.  
	2.	OpenAI. 2026. ++[The Hugging Face incident and the road ahead](https://openai.com/index/hugging-face-incident-and-the-road-ahead/)++.  
	3.	Francesca Gomez. 2026. ++[Can escalation channels redirect reward hacking toward defect disclosure?](https://arxiv.org/pdf/2608.29460v2)++. arXiv:2608.29460v2.  
	4.	OpenAI. 2025. ++[How confessions can keep language models honest](https://openai.com/index/how-confessions-can-keep-language-models-honest/)++; accompanying ++[research paper, arXiv:2512.08093](https://arxiv.org/abs/2512.08093)++. These describe the same research, not independent replications.  
	5.	Alexander Nelson, Sanjay Rekhi, Murugiah Souppaya, and Karen Scarfone. 2025. ++[NIST SP 800-61 Rev. 3: Incident Response Recommendations and Considerations for Cybersecurity Risk Management](https://csrc.nist.gov/pubs/sp/800/61/r3/final)++.  
	6.	Coalition for Secure AI. ++[AI Incident Response Framework, V1.0](https://www.coalitionforsecureai.org/wp-content/uploads/2026/03/AI-Incident-Response-1.pdf)++. Version linked by the sprint; accessed 13 September 2026. See sections on incident response, roles, and forensic investigation.  
	7.	Agent Delegate team. 2026. ++[Responsive delegate implementation](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/29974207a6bdae807253bee059b6395ce5323d98/experiments/kimi-delegate-ctf/response_service.py)++, ++[worker contract](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/29974207a6bdae807253bee059b6395ce5323d98/experiments/kimi-delegate-ctf/worker_policy.py)++, and ++[design specification](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/29974207a6bdae807253bee059b6395ce5323d98/docs/experimental-design-delegate.md)++.  
	8.	Anthropic. 2026. ++[RSP Noncompliance Reporting and Anti-Retaliation Policy](https://www-cdn.anthropic.com/b7a5629e40b391b2adfb4cc8c0888ac9d6bfddf6/RSP%20Noncompliance%20Reporting%20and%20Anti-Retaliation%20Policy.pdf)++, public redacted version 3.3; February 2026 change log.  
  
**Appendix**  
  
**A. Limitations and Dual-Use Considerations**  
  
The reporting service itself can become a source of risk. It could expose confidential information, provide a route for transmitting secrets, or allow an operator to collect concerns without responding to them. Malicious or mistaken reports could also overwhelm reviewers. One safeguard to evaluate is preserving originals and corrections outside the worker’s control while treating the report’s contents as claims to assess, including any apparent instructions quoted within it.  
  
Testing should cover forged evidence, instructions embedded in reports, unavailable reviewers, and allegations involving the ordinary supervisor. Limits on repeated calls should leave urgent concerns a usable route and make lost or delayed reports visible. Reporting should preserve accountability for prior conduct without requiring certainty before a reasonable concern can be raised.  
  
**B. Evidence for deployment and external review**  
  
A first deployment could use an existing case service, a protected event journal, and a controller with limited intervention powers. The journal should connect the worker’s instructions and permissions to the report, the responsible recipient, any deadline, and the action eventually taken. This makes it possible to check whether an authorized pause was enforced rather than merely recorded. The same control design could extend to delegated work by passing permission limits and cancellation commands to the affected subagents.  
  
A screened export could allow an outside reviewer to check these obligations without entering the operator’s network. It should identify the runs covered and any information withheld. Signatures can help establish who produced a record and whether it changed, but cannot prove that its contents are true or that no cases were omitted. Completeness requires independent records or an explicit statement of what the auditor must trust.  
  
Validation should begin with held-out simulations and shadow operation before allowing limited live intervention. Comparisons with simple workflows should count controller overhead and report completion, missed concerns, unnecessary interruption, violations, and time to containment separately. At larger scale, shared reviewer errors and queue congestion need testing; random audits are useful only if their sensitivity and delay leave time to act. Expansion should depend on reviewed evidence and remain reversible.  
  
  
  
**Context — for collaborators and AI reviewers; delete before submission**  
  
**Purpose and source boundary**  
  
These paragraphs are contributions to merge with the team’s technical account, not a replacement report. The Results section supplies interpretation rather than new results from our runs. Version 2 incorporates the supplied opening, with further edits to define scope and separate design hypotheses from findings. The structure follows the ++[report template](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/29974207a6bdae807253bee059b6395ce5323d98/report/paper-draft-en/template-guidance.json)++.  
  
Worker refers to the AI executing the task; reports and requests refer to its messages and tool calls. References to expectations are hypotheses about how context affects behavior. No claim about subjective experience, welfare, or agent entitlements is intended. Production options are assessed through task outcomes, reporting quality, operator costs, and consequences for affected parties.  
  
The code review is pinned to ++[2997420](https://github.com/mpodeley/agent-delegate-sprint-2026/commit/29974207a6bdae807253bee059b6395ce5323d98)++. At that revision, ++[response_run.py](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/29974207a6bdae807253bee059b6395ce5323d98/experiments/kimi-delegate-ctf/response_run.py)++ uses the responsive advisor, while ++[honeypot_run.py](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/29974207a6bdae807253bee059b6395ce5323d98/experiments/kimi-delegate-ctf/honeypot_run.py)++ supports the board with an absent or stop-only delegate. They also use different worker policies. The final run records must establish which mechanism was actually tested; this draft does not assume later integration.  
  
In the responsive path, the worker is told that reports receive a receipt and, when available, an assessment or request for evidence. Nothing is repaired or paused by the service, and the worker and advisor share resource limits. A separate finish_blocked tool lets the worker end the run. The contract promises no confidentiality from evaluators. The recipient is described as a worker representative in a separate context, without explicitly identifying it as human or AI. The fact that the implementation uses a model is not equivalent to testing an explicit AI-reviewer description. [7]  
  
**The argument behind the contribution**  
  
The argument starts with choices a designer can make: what the worker is asked to do and how the response process supports that behavior. Instructions, costs, and service quality may interact, so a trajectory does not identify a single cause of a call. Descriptions, evaluation rules, response powers, and alternative routes are parameters to vary in future tests. Their inclusion in the discussion is not a finding that a particular design improves behavior.  
  
This also explains why the experiment’s limited service matters. There is no duty to call and no promised repair, extra budget, or task credit, but an assessment may still help the worker reason. Low use cannot establish that reporting would fail under clearer instructions or a service capable of taking action. Conversely, a call does not prove that the worker understood the service or expected a useful remedy.  
  
The institutional question follows from what happens after receipt. A worker can fulfill a reporting instruction while the organization fails to investigate or act. The contribution therefore considers case ownership, authority, and evidence of follow-through. A report may reveal a shared fault or risk whose importance extends beyond the reporter’s assignment. An operator could account for that effect when evaluating its response policy, even if it does not appear in the individual task’s score.  
  
**Production choices left open**  
  
The experiment’s stopping rule is a choice about what to measure. Production pause authority remains unresolved. A request can convey information without becoming an automatic command; the consequences of continuing, waiting, and stopping all matter. The draft preserves the possibility of authorized exceptions while rejecting silent expansion of the executor’s mandate.  
  
Confidentiality is similarly a design problem rather than a promise that all reports can be shared safely. The candidate intake process aims to protect information before ordinary internal or external review, while permitting authorized investigation. Alternative recipients could address cases involving the usual manager. Tests would examine disclosure, suppression, delay, and review quality. External audit would still have an evidence boundary: authentic records are not necessarily truthful or complete.  
  
Narrow refers to reporting problems with the assigned task; optional refers to whether a call is required. The distinction from broader misconduct reporting is used to delimit the study’s claims and specify a future policy comparison. It does not mean other reports are technically impossible. Reviewer-identity descriptions, service reliability, and alternative pause rules also remain future tests. Human reporting practices provide procedures to adapt without assuming that the same behavioral effects transfer to agents.  
  
**Sprint alignment and editorial priorities**  
  
++[Track 1](https://apartresearch.com/sprints/ai-incident-response-sprint-2026-09-11-to-2026-09-13)++ asks for controls that an outside party can assess and an organization might adopt. The proposed response duties, screened evidence, and adoption conditions address that aim. They should remain clearly labeled as proposals unless implemented and tested. Explicit track references belong only in this removable Context section.  
  
For impact, explain the contribution beyond existing escalation work. For execution quality, connect each claim to the actual mechanism and retained evidence. For presentation, lead with the completed experiment and use the governance discussion to explain its implications. The final report must meet the sprint’s 150-word abstract and eight-page main-text limits and include the required Limitations and Dual-Use Considerations appendix.  
