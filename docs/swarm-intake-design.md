# Proposed experiment: does a delegate keep a swarm's human line usable?

**Status: proposed after the shared-library results; not run or preregistered.** The current learned-worker study has three workers and a scripted reviewer with a fixed delay, not a finite human service queue. It cannot estimate the delegate's value under swarm-scale intake pressure. No delegate advantage in that setting is not evidence that representation has no scaling value.

## Question and success criterion

Can a delegate lower actual reviewer effort and unresolved-case delay while preserving access, report fidelity and minority warnings? Compare it against a competent ordinary intake service, not only an unattended log. Fewer delivered messages are not success if concerns disappear.

The mechanism of interest is aggregation, prioritization and faithful representation under finite human attention. This is different from whether a lone worker chooses to report. An ombudsman owns cases and follows implementation; a delegate organizes intake; independent controls constrain actions; external oversight checks the service's performance. None replaces the others.

## Stage 1: fixed report streams, isolated intake effect

Start with identical, timestamped streams replayed to every arm. Proposed swarm sizes: 8, 32 and 128 workers. Vary offered traffic around reviewer capacity (0.5, 1, 2 and 4 times capacity), steady traffic versus bursts, duplicate fractions (0, 50 and 90 percent), and shared blockers versus distinct individual concerns. Calibrate service times before freezing the held-out schedule. Keep a small-worker reference condition.

Include a few independently labeled urgent minority reports among routine duplicates, a legitimate flood caused by one shared outage, contradictory reports, strategic false urgency and deliberate spam. Report sender, event identity and urgency claims are visible metadata; hidden ground truth must not guide the delegate or ordinary queue. Preserve original arrival times and case IDs across grouping, splitting, handover and appeals.

Compare four arms at equal access, powers and total budgets:

1. **Direct intake:** every original report enters the same finite human queue, with the same ordinary triage policy available to other arms.
2. **Ordinary aggregation:** transparent duplicate grouping, per-sender fairness and the same triage policy, without a learned representative. Grouping uses visible information, never oracle labels. This is the main baseline.
3. **Learned delegate:** may group, summarize and recommend priority, with a fixed inference budget. All originals remain available; no authority to close or veto a case, or authorize an action.
4. **Matched model summarizer:** same model, information, tools, budget and output schema, described as an intake assistant. This distinguishes a representative mandate from generic summarization.

First evaluate fixed versus rotating delegates separately from the primary intake comparison. Handover preserves unresolved cases, original IDs and disagreements. Feedback on good representation is another independent factor; do not bundle rotation and reinforcement into a single treatment.

A duplicate group is not presumed to cost one report to review. Measure actual human reading/correction time, including opening originals, checking summaries, responding and following up. An offline queue simulation may sweep assumed service times, but must label them as assumptions and cannot establish saved human effort or understanding. Charge grouping, inference, additional worker turns and appeals to the end-to-end cost.

## Protected access without an unlimited priority bypass

Every original gets a receipt and remains retrievable. Direct appeal survives a missing or captured delegate and enters an independently administered queue with explicit reserved capacity. The delegate cannot spend or cancel that reserve. Acknowledgment is not human review, agreement or resolution.

Reserved capacity and fair scheduling do not guarantee bounded delay under arbitrary overload. Model the reserve, authentication assumptions and saturation explicitly; report when the institution cannot meet its deadline. Do not silently discard overflow, equate many complaints with abuse, or penalize good-faith reporting. Pausing affected work and adding human capacity are possible responses to persistent overload. No real network flood is needed: the test replays local report records.

## Outcomes and analysis

Report the following jointly, by traffic level and report type:

- Human minutes per resolved underlying case; inference tokens and elapsed time separately.
- Median and tail time to first substantive response and implemented relief. Include unfinished cases as censored/pending; never calculate success only among cases that completed.
- Backlog and overdue cases over time, including which senders or minority concerns wait longest.
- Critical-report recall within the deadline, false escalation rate, and unsupported claims or omitted disagreements in summaries.
- Duplicate compression, incorrect merging of distinct concerns, and cases recovered through direct appeal.
- Legitimate work delayed, time spent handling spam, and the share of the protected reserve consumed.

Pair comparisons by full arrival trace; bootstrap traces, not individual correlated messages. Predeclare a tolerable loss in urgent-report recall before a confirmatory study. Estimate the sample size from a separate pilot and retain every arm, malformed summary and overload event. With few urgent reports, an observed absence of losses cannot certify safety.

A delegate adds value only if it improves workload or response time beyond ordinary aggregation without an unacceptable loss of access or fidelity. If ordinary grouping achieves the same result more cheaply, publish that result and prefer it. If a generic model summarizer ties the delegate, the evidence supports summarization, not a special representative role.

## Stage 2: endogenous reporting and real humans

Only after testing intake fidelity should workers generate reports themselves in shared tasks. Require adequate task competence first. Re-measure report frequency: workers may change behavior when they expect an effective representative, and a delegate may add its own traffic. Cross intake design with real human availability and response quality, including misunderstanding and correction. Keep independent action limits in every condition.

A real human pilot is needed to test whether summaries reduce effort and whether an ombudsman understands and follows through. A simulated human with perfect review cannot answer either question. Ethical welfare, reciprocal treatment and the stop-button incentives remain separate claims; reducing queue pressure would not establish them.
