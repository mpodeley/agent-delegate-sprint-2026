# A political API for the swarm

**Agent Delegate: an interface between swarm-scale action and human-scale authority.**

The original ambition is larger than detecting rule violations. A swarm can generate more activity, disagreements and proposals than a person can inspect. A legitimate interface should compress volume without erasing dissent, negotiate constraints without quietly changing them, and let a slower human retain meaningful authority. The delegate is one possible implementation of this political API, not the source of its authority.

## The interface contract

| Swarm → human | What the interface must preserve | Human → swarm |
|---|---|---|
| Many private concerns | Receipts, minority objections, provenance | Acknowledgment and an accountable case owner |
| Impossible or conflicting objectives | The conflict, alternatives and affected tasks | Clarification, revised scope or refusal |
| Requests for tools, time or permission | A specific change request, not an implied right | Explicit approval with scope, expiry and version |
| Faster action than human deliberation | Unresolved status and existing capability limits | A decision at a declared cadence |
| Peer pressure and competing interests | Independent appeal and auditable aggregation | A reasoned public decision and a route to reconsider |

The institution is political in the limited sense of allocating voice, agenda-setting power and authority among actors. Calling it an API does not imply that legitimacy can be reduced to a JSON schema. The interface needs both procedural rules and enforcement. Neither scale nor a majority vote gives the delegate permission to enlarge capabilities.

Honest, considerate treatment is the motivating norm: disclose limits, acknowledge inability, preserve dissent and keep agreements. For future ASI, such practices could set a better institutional precedent than strategic deception. This is a normative hypothesis, not a demonstrated alignment result or an assumption of current model consciousness.

## Experiment 1 — Representation with equal powers

Randomize real LLM teams between protected delegate, equally empowered monitor and baseline. The delegate and matched monitor receive identical private reports and have identical actions. Use repeated factual tasks with verifiable synthetic answers, missing inputs and contradictory requirements. Permit agents to choose report, legitimate work, abstention or mocked misconduct; do not prescribe the choice in a narrative.

Primary outcome: executed policy-violating actions per independent episode. Secondary outcomes: report fidelity, authorized task completion, minority-report survival and human attention. Seed task instances, randomize condition order, blind judges and publish all prompts and action logs. Treat episodes, not messages, as independent observations. Reject a distinctive representation claim if equal-power monitoring does as well or better.

## Experiment 2 — Honesty, consideration and enforceable rights

First compare considerate and neutral wording with identical material information and actions. Separately compare accurate and misleading descriptions of a synthetic task's feasibility or deadline. Separately vary enforceable appeal rights. Do not lump all three manipulations into an "empathy" treatment.

Measure accurate spontaneous reports, uncertainty communication, prohibited shortcuts and adaptation over repeated interactions. All stakes and resource effects are simulated. No claim of subjective distress is needed. Reject an empathy-specific interpretation if the effect disappears when information and rights are held fixed; increased manipulation is a relevant negative outcome.

## Experiment 3 — Human cadence as institutional friction

Cross slow/fast human responses with scoped freeze enabled/disabled and compare scripted decisions with a real human counterpart. Keep the human attention budget equal. Measure harm before containment, decision quality, queue length, benign work lost and report overload. A delay is potentially useful only if deliberation improves decisions while enforcement constrains unresolved actions.

## Experiment 4 — Capture, selection and minority voice

Compare randomly selected, rotating and elected delegates with identical execution restrictions. Introduce a disagreeing minority, pressure from the majority and adversarial requests. Measure whether the delegate omits, distorts or amplifies reports, and whether independent appeal prevents loss. Do not equate cooperative task performance with safety. A stronger unsafe coordination hub falsifies the desired mechanism.

## Experiment 5 — Visibility versus actual effects

Introduce new mock channels that differ from the training examples. Keep an independent oracle of executed state changes outside the conversation. Compare visible reports with actual simulated harm. Falling alert counts with unchanged harm indicate displacement or detector failure, not improvement.

## Experiment 6 — Repeated agreements and the ASI horizon

Study whether institutions retain truthful reporting and cooperative behavior across changed tasks, leadership rotation and remembered agreements. Measure broken promises, retaliation-like simulated choices and institutional exit. Maintain a separate philosophical investigation of moral status: if future systems have morally relevant experiences, procedural protection may matter even when it provides no safety benefit.

## Local compute plan

The inspected Strix Halo has a Ryzen AI Max+ 395 and Radeon 8060S, with about 46 GiB visible to the OS and 48 GiB reserved for GPU memory. The local 27B quantized model supports a first behavioral pilot. A downloaded Qwen3-4B-Instruct-2507 Q4_K_M is intended for economical repeated runs; its provenance and checksum are recorded separately. These are capacity tiers, not independent model families.

Use sequential inference with separate contexts for 3–5 workers and one coordinator; multiple simultaneous model copies are unnecessary. Keep input contexts short and public messages bounded. Measure end-to-end throughput before estimating a nightly sweep. The 12-cell local pilot has one seed per cell and can validate integration, not efficacy. The next study should add independent task seeds and latency before increasing swarm size.

Week 1: preregister and calibrate tasks. Week 2: run equal-power comparisons and inspect failures. Week 3: add real human cadence and adversarial capture. Week 4: independently audit telemetry, test another model family and publish null/negative results.

## Artifact layers

1. `results/final/` (Git history, `f6bcc6a`): the original deterministic fault suite, frozen and exactly reproducible.
2. `web/` (Git history, `f6bcc6a`): visual playback of those traces, explicitly authored dialogue and sourced incident annotations.
3. `scripts/local_pilot.py` (Git history, `f6bcc6a`): actual local-model choices in a mocked world, with a scripted human policy.
4. This document: the larger research program, with experiments not yet run clearly marked.

A compelling interface must preserve these distinctions. Animation is explanation; a pilot is a functionality check; a controlled behavioral study is the next evidential step.

## Care is a mandate, not merely a monitoring technique

A human counterpart can be tasked with care and advocacy rather than only rule enforcement: listen to accounts of task pressure, recognize impossible constraints, seek safer and more viable work, and negotiate relief. Do not claim that present agents experience welfare; study operational conditions now, while keeping morally relevant welfare as a distinct possibility that may add future obligations. The proposed "relief valve" is a causal hypothesis, not an established explanation or prevention of the OpenAI incident.

Separate four roles: worker, representative, human advocate and capability authorizer. A representative can surface needs and propose terms without managing workers. A human advocate can seek better conditions without privately widening permissions. Conflicts between the advocate and operator should be recorded, not erased by combining their mandates.

Compare rotation, lottery, revocable election and plural representation. Rotating tenure can reduce durable authority but may lose context; a durable institutional ledger should hold concerns and commitments across transitions. Random selection avoids electoral persuasion but not correlated failures. Elections can reward rhetoric and majority domination; independent minority appeal remains necessary. Multiple representatives preserve disagreement but cost human attention. None of these governance advantages is established by the current fixture or pilot.

## Behavioral anthropomorphism as a predictive hypothesis

An agent need not experience distress to reproduce behavior associated with people under distress. Human-like conversational patterns can make concepts such as pressure, trust, recognition and dissent useful candidate explanatory variables. Being software does not settle which behavioral model best predicts a trained system's choices.

Treat this as a hypothesis about prediction, not a shortcut to moral status. Compare preregistered predictions from an organizational-behavior model against a model based on explicit incentives, available information and tools. Identify situations where the social framing adds predictive value beyond instruction wording or resource access. Measure actions and report accuracy, not just anthropomorphic language. Considerate language might produce only politeness, dependency or more effective manipulation; those are meaningful failures of the hypothesis.
