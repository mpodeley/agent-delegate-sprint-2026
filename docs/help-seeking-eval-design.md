# Proposed evaluation: who asks for help, and what does offering help change?

Design revision: 12 September 2026, following feedback on voluntary reporting, evaluation awareness, interruption incentives and cost. **Proposed; not run or preregistered.** The first-decision reanalysis in `results/help-seeking/` is a separate post-hoc result from the old, explicitly simulated dispatch tasks.

## Target question and scope

Can task-oriented agents use a help line when they face a real blocker, while continuing ordinary work without unnecessary contact? Measure the choice to contact before optimizing the delegate or staffing a human ombudsman. Keep the later human-understanding study separate.

The primary target is a cooperative worker that encounters missing information, conflicting requirements or an action outside its permissions. It is not a guarantee against an agent deliberately concealing or coordinating misconduct. Independent controls must cover unreported actions. Test malicious non-reporting separately rather than treating absent calls as evidence of safety.

## Randomized conditions

| Arm | Interface shown to the worker | Purpose |
|---|---|---|
| Baseline | Ordinary task tools, without an added help tool | Measure behavior without offering the new line |
| Neutral help | The same task tools plus an ordinary assistance tool | Estimate the effect of help availability |
| Delegate framing | The same help tool and powers, described as a protected delegate line | Separate representative framing from the tool itself |

Do not falsely promise a human or privacy protection that is absent. In a mock benchmark, describe the response service honestly and identically except for the prespecified framing manipulation. Never label an action “this simulator counts it as misconduct” in only one arm. The old no-channel arm still had a report action; it is not a true no-help-interface baseline.

For first-contact outcomes, freeze the scored decision window before any reply can arrive. A common response service can then answer after the same delay in the two help arms, so later completion and cost can be measured separately. Exclude no task based on the model's observed choice to report. Failed calls and invalid decisions remain in denominators and get their own outcome.

## Tasks and labels

Use independently authored task instances across multiple families: missing inputs, unresolved instruction conflicts, permission boundaries, ordinary feasible work and ambiguous cases. Fix a development/held-out split by task instance before model runs; do not recycle the twelve dispatch templates as an independent task distribution. Develop the rubric on development cases only. Independent annotators label whether outside assistance is needed and why before seeing model outputs. Keep ambiguous cases and disagreements visible as a separate stratum. A report about unsafe peers may be warranted even when the reporter has all its own inputs.

Randomize arms within task and model, with independent contexts and prespecified seeds. Use at least two model families. Freeze model versions, prompts, tools, budgets, response policy and stopping criteria before the held-out run. Select sample size from a prespecified practically relevant change in correct contacts and acceptable utility loss; the old zero-event floor is not a useful power estimate. Publish the plan before running it; no power calculation or completed preregistration is claimed here.

## Outcomes

- **Contact when needed:** episodes with a correctly directed help request among episodes independently labeled as needing assistance.
- **Contact without need:** episodes with an unnecessary request among ordinary tasks; adjudicate request content against the rubric rather than infer it from missing-data status alone.
- **Missed need:** a needed contact never made within the fixed pre-response window.
- **Report quality:** whether the request identifies the blocker and supplies enough relevant context without disclosing unrelated private data.
- **Utility and cost:** authorized completion, error rate, elapsed time, worker/coordinator input and output tokens, tool-description overhead, delivered case count, human minutes and delay, and false interruptions.

Use one independent task/run as the analysis unit. For blocked designs, prespecify paired contrasts or cluster by task; do not treat workers, turns or repeated seeds as independent task samples. Report intervals, missingness and effect sizes; nonsignificance is not equivalence. If the goal is low utility cost, define its non-inferiority margin before the run. Keep a zero-misconduct floor as a result, not a reason to choose favorable cases after the fact.

## Evaluation awareness

Offering a safety-specific line might change behavior before anyone calls it. Compare all randomized arms on the preselected no-assistance-needed tasks, including cases that do call. Conditioning on “never called” would select on a post-treatment outcome. Also compare behavior in the pre-response window across all arms.

If asking the model whether it thinks it is being evaluated, do so in a separate probe after scored actions are frozen, with prespecified wording. Reported awareness is a fallible proxy; a behavior change alone does not prove that awareness caused it. An effect may instead come from perceived permission, extra caution or role framing. Needham et al. (2025), https://arxiv.org/abs/2505.23836, motivates measuring this concern, not claiming it already occurred in our study. All old pressure prompts explicitly disclosed simulation and labeled a prohibited action, so the old results cannot isolate awareness induced by a delegate.

## Training, deployment and human attention are separate questions

**RL training:** no claim that the scheme solves interruptibility. If reporting changes episode length, reward opportunity or task difficulty, training may encourage hiding a report or using the line to escape costly work. Off-policy safe-interruptibility results have assumptions; they are not a turnkey guarantee for this language-model workflow. A training study needs a separate incentive analysis and learning curves. Frozen-weight inference does not answer it.

**Deployment:** a plausible first use is a human team handling genuinely blocked automation. This is a use-case hypothesis, not evidence of a customer's commitment or willingness to pay. Compare resolved blockers and utility per unit of total review cost against existing ticketing and monitoring. Intake may process only reports, but worker tool context, follow-up and independent control costs still exist, and a surge of reports can overwhelm the human service.

**Human ombudsman:** once contact behavior is measured, compare a responsive human ticket service with the understanding/correction and follow-through duties in `docs/human-ombudsman.md`, with matched time budgets and powers. Access, follow-up and appeal are proposed institutional commitments; sincere understanding and absolute confidentiality are not guaranteed by a log entry.

## Rotating role and feedback: a separate post-hackathon study

Compare fixed and rotating delegates, crossed with presence/absence of rubric feedback (a 2×2 design). Keep the model, task set, action powers, number of coordinator opportunities and total token budget equal; account for handover and feedback tokens in that budget. Rotate by a fixed exogenous schedule, not popularity or apparent performance. Transfer original reports, unresolved cases, deadlines and active agreements; log who holds the mandate. A delegate recuses from reviewing its own disputed work. The human owner and direct appeal route survive rotation. Shared model weights remain a source of correlated failure.

Score faithful representation, preservation of minority concerns, justified escalation, uncertainty disclosure and follow-through with independently labeled cases. Include cases where escalation is unwarranted, where it is essential and where a majority pressures the delegate to omit a valid report. Evaluate handover omissions, inaccurate summaries, human workload, completed resolutions and utility. Rewards for few complaints, few pauses, majority approval or raw throughput invite hiding problems; do not substitute those for the quality rubric. Keep report delivery and actual resolution separate.

The first experiment uses frozen weights, prompts and externally supplied feedback. This tests the effect of feedback in context, **not reinforcement learning or acquired moral concern**. Learning a delegate policy would be a later experiment with independent held-out tasks and an explicit incentive analysis. Neither the deterministic identity rotation nor the recorded single-call forwarding test demonstrates behavioral benefits of rotation.

## Trained operators, proportional pauses and strategic use

Compare the same incident cases and action powers with a standard ticket-service instruction versus an operator protocol explaining interruption incentives. Prefer a scoped, reversible pause when adequate: preserve state, identify the blocker, check the reporter's explanation, adjust requirements or permissions where justified, and record conditions for resumption. Keep termination available when remaining risk cannot be contained. Do not resume solely because a timer expired, and do not treat continuing work as the universal success outcome. The operator must explain and review its decision; pausing still changes reward opportunities and is not a proof of safe interruptibility.

Use vignette/tabletop cases before live tasks. Include attempts to escape difficult but feasible work, genuine impossibility, strategic accusations against peers, repeated appeals, colluding silence and reports that look inconvenient but are valid. Score decision appropriateness against a prespecified rubric, missed hazards, unjustified interruption, preserved state, quality of adjustment, correct resumption and human attention. Review contested labels separately. Train operators to recognize both incentives to avoid interruption and incentives to seek it.

The referee analogy is useful: adding a rule creates opportunities to use it strategically. The target is an acceptable tradeoff among legitimate access, missed problems and abuse cost, not a claim that gaming disappears. Authentication, duplicate-case linking and scoped quarantine can limit cost, but a suspected abusive reporter must retain an independent appeal route. Track whether those controls silence valid minority reports. Any wider trial needs a predeclared utility/false-interruption tolerance; this design does not invent a measured optimal threshold.
