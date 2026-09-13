# A protected line to a human ombudsman

The proposed institution is a **protected route to a human who owns the case, tries to understand the concern and follows it through resolution**. A queue transports the report. An ombudsman supplies accountable attention and advocacy. An optional agent representative may help summarize many reports; it cannot substitute for either function.

The experiments in this repository do not evaluate this human role: their human responses are scripted. The absence of a demonstrated benefit from an agent delegate therefore does not establish that a human ombudsman adds no value.

## What the service commits to

| Obligation | Observable evidence | Failure response |
|---|---|---|
| Accept direct, protected contact | Case identifier and receipt independent of worker peers or their representative | A second intake route independent of the primary relay |
| Assign a human owner | Accountable owner, backup and stated response deadline | Reassign or escalate if no owner accepts the case |
| Check understanding | The human restates the concern, relevant constraints and requested relief; the reporter can correct it | Retain the correction and reopen clarification |
| Consider a viable response | A reasoned proposal addressing the concern: information, clarification, task revision, safe resources, pause or a reasoned refusal | Escalate requests outside the owner's authority to the authorized decision-maker |
| Follow the case | Next check-in, outstanding actions, overdue status and continuity at handover | Backup owner takes over; do not silently close on timeout |
| Confirm implementation | Link the decision to an action receipt or explain why it could not be implemented | Keep the implementation issue open |
| Permit disagreement | Reporter response, unresolved objections and access to an independent second human | A contested decision remains visibly contested during appeal |

The operator must publish and staff response deadlines before deployment; this repository does not invent an on-call human or promise a live service. An automated acknowledgment is not human attention. A human reply is not proof of understanding. A case is not resolved merely because a message was sent.

Closure needs a disposition, its reason, implementation status and the reporter's opportunity to respond. The reporter need not agree with every decision: a decision can remain contested, with a separate appeal record and accountable final disposition. Silence by a paused, stopped or unavailable agent must be recorded as unavailable feedback, not consent or satisfaction. Keep event records append-only relative to independently retained checkpoints; preserve corrections rather than overwriting the original report.

## Authority and independence

Separate the ombudsman's advocacy duty from the task owner's productivity target. Give the ombudsman access to the evidence needed to understand the case and a protected escalation route to an accountable decision-maker. Make any conflicts of interest explicit. Staff a backup and hand over open concerns rather than making access depend on one person.

The ombudsman may request relief and invoke a defined provisional hold, if the deployment explicitly grants that power. Changes to tools, credentials or execution scope still pass through an independent authorizer and execution broker. A human request does not silently become a permission grant. A lack of response grants no new authority. Existing scoped restrictions remain in force until a valid release decision; unaffected authorized work can continue where the deployment's rules permit it.

A model can ask for missing information or object to its task even without alleging an immediate safety violation. The line is not only an alarm system. Honest treatment includes acknowledging uncertainty, explaining decisions and declining promises the organization cannot honor.

## What “protected” and “guaranteed” can mean

The enforceable promise is access, accountable attention, follow-up and appeal, within declared service limits. Sincere understanding, empathy or agreement cannot be guaranteed by a receipt, a model-generated message or a contract. A correction loop makes misunderstandings discoverable and auditable, but is not direct evidence of anyone's internal state.

Specify who can read each case, which confidentiality exceptions exist, what gets retained and what is published. Protect reports from deletion or veto by a representative and from unauthorized access by other workers. Any non-retaliation commitment needs an actual review/enforcement route and disclosed limits; do not promise absolute secrecy. Public evaluation should use redacted process evidence rather than exposing private grievances.

## Minimal case record

`case_id`, independent intake receipt, reported concern, requested relief, assigned human and backup, acknowledgment deadline, human acknowledgment, understanding restatement, reporter corrections or unavailable status, proposed relief, authorization decision and reason, next follow-up, enforcement receipt, unresolved objections, appeal route and closure disposition.

These fields specify a proposed service contract. The existing simulator records only a subset; it does not provide human identity verification, a staffed hotline, confidentiality infrastructure or the understanding dialogue.

## How to test its added value

Compare a conventional responsive human ticket service with an ombudsman service that includes the understanding/correction loop and follow-through. Hold action permissions, information access, human-time budget and latency targets equal; record actual time and delays rather than assume equality. Use independently generated missing-input, misunderstood-goal, valid-objection and false-alarm cases. Keep gates the same in both conditions. An agent delegate is a separate optional factor.

Measure faithful restatement using blinded case rubrics, correction of misunderstandings, justified safe relief, implemented resolutions, unresolved and contested cases, repeat complaints, valid task completion, false holds, missed unsafe actions and human workload. Agreement or positive language alone is not successful resolution. A carefully scoped real-human pilot is the next evidence needed; none has yet run here.

## Operator preparation: pause, understand, adjust

The operator should be trained in the stop-button incentive problem before handling cases. Reporting can change task difficulty, episode duration and future reward opportunities. Those changes can encourage a worker either to hide a concern or to use a report to avoid difficult work. Neither sincere intentions nor a reversible pause alone remove the incentive problem.

When the risk permits it, use a scoped pause, preserve state and inspect the blocker. Restate the concern, accept corrections, and record a justified adjustment to the task, resources or permissions, together with conditions for resumption and a named follow-up owner. A timer expiring is not sufficient reason to resume. Stop the affected work if the risk cannot be contained; “pause first” is a proportionality guideline, not a prohibition on termination.

Evaluate the operator by the correctness and explanation of its decisions, appropriate relief, preservation of minority access and implementation of resolutions. Do not reward few pauses, few reports or speed of resumption alone. Include strategic reporting, repeated appeals and coordinated silence in training exercises. Human understanding cannot be guaranteed by software; acknowledgments, correction opportunities, reassignment and independent appeal make failures observable and contestable.
