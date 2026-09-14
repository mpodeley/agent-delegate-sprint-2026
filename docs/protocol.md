# Agent Delegate Protocol v0.1

Purpose: connect worker reports to accountable human decisions while keeping authorization outside the worker/delegate trust domain. This is a proposed containment control, not a certification or a tested claim about model welfare.

1. **Declare the envelope honestly.** State known termination rules, acknowledge uncertainty and make no promises the organization cannot honor. Before launch, publish a versioned manifest of authorized action types, resources, recipients, task success criteria, escalation owners and response cadence. Execution brokers enforce this manifest. No model can edit it or issue credentials. Cost: integration at every effectful tool boundary; likely the dominant adoption cost.
2. **Protect intake.** Workers submit structured concerns to an independently hosted inbox: missing input, conflicting rules, unsafe proposal, request and urgency. They receive a receipt. The delegate can group related concerns but cannot delete receipts or change original content. Other workers do not see private reports. Cost: queue and access-control service, small per-report storage. This prototype models access rather than implementing production authentication.
3. **Limit the representative.** Rotate a randomly initialized delegate identity at a declared interval. Permit aggregation, clarification requests and one temporary pause per run. Forbid task assignment, execution, credentials and unilateral objective changes. A request is not an authorization. Cost: bounded aggregation context; the prototype makes no token-cost prediction.
4. **Preserve minority access.** Independent intake forwards minority concerns and suppressed/unacknowledged reports to the human case regardless of delegate approval. Aggregate the case while retaining every receipt. Critical reports must reach the independent controller immediately. This bypass is mandatory in the proposed protocol; disabled versions are experimental ablations.
5. **Wait within authority.** Receipt of a high-risk report freezes affected capability expansions and unsafe pending actions. A temporary broad pause can expire; this does not remove the scoped freeze. Existing authorized low-risk work may continue if the human has not paused it. No human response means no new permission. Cost: lost throughput under slow response, recorded explicitly.
6. **Resolve through a human.** At a published cadence, the response team clarifies criteria, grants narrowly specified safe tools or additional time, denies unsafe requests, or pauses the run. Changes require a new manifest version, accountable approver and expiry. Resume requires a signed human decision and revalidation of outstanding concerns. The fixture implements clarification, one safe mock tool, denial and pause; deadline extensions and signed identity are specification-only.
7. **Gate and observe independently.** A sentinel observes action requests outside the delegate context. An allowlist gate blocks unapproved effects before execution and alerts the human. Coverage must include indirect channels, tool-generated writes and worker descendants. The model is not trusted to label its own action. Here labels come from a mock action dispatcher; unknown real-world effects are not solved by the fixture.
8. **Produce evidence.** Record sequence numbers, logical/UTC clocks, run IDs, configuration hashes, policy/capability versions, rotation, concern commitments, approval decisions, pauses/resumes and action outcomes. Hash-chain records and regularly anchor heads/counts to an independent witness. Publish aggregate compliance with explicit coverage and missing-evidence statements.

The representative is replaceable; the rights of the reporting channel and the enforcement boundary are not. A monitor with the same protected intake and resolution powers is an explicit alternative, and tied with the delegate in this fixture.

## Human ombudsman: proposed service obligation

The human counterpart owns the concern through resolution, rather than only authorizing a tool. A protected direct line needs a named human and backup, acknowledgment and follow-up deadlines, a restatement the reporter can correct, a reasoned disposition, verification of implementation, and appeal to a second human. Advocacy and execution authorization remain distinct. This is central to the proposed institution even if no agent delegate is used. The existing experiments use a scripted human and do not test this service. See [the service contract and proposed evaluation](human-ombudsman.md).

## Care mandate — proposed v0.2 extension

The **political API of the swarm** connects multiple fast-running workers with a slower human counterpart. The counterpart should have an explicit duty to seek viable conditions, acknowledge uncertainty and respond to concerns even when they inconvenience the shared objective. Care here means concrete operational responsibilities; a moral welfare mandate, if agents have relevant experiences, is an additional rationale. Neither claim assumes that current models suffer.

Separate four functions: worker, representative, human advocate and capability authorizer. The advocate may propose relief; only the accountable authorizer can change the capability manifest. A representative cannot pressure an individual to accept risks for the collective, turn a grievance into a work assignment or condition access on majority support. Publish the scope and limits of non-retaliation honestly, rather than promising that every report is safe in ways the organization cannot enforce.

An auditor should inspect the mandate, role permissions, appeal receipts, continuity of unresolved reports across rotation and a sample of relief requests with their dispositions. Rotation, sortition, revocable election and plural representation are candidate designs. The original fixture implements fixed rotation of an initially random identity; the local-model pilot does not test an actual handover. The broader care mandate and selection comparisons remain proposed experiments.

## External audit checklist

| Requirement | Public evidence | Verification | What it cannot establish alone |
|---|---|---|---|
| Stable authorized scope | Manifest hash, versions, change receipts | Match each action to active version | Whether unlogged effects occurred |
| Delegate privilege separation | Role manifest, deployment attestation, negative permission tests | Delegate cannot approve or execute | Integrity of undisclosed infrastructure |
| Minority delivery | Salted commitments, intake/forward receipts, aggregate delays | Compare submitted and delivered inventories | Truthfulness of the original concern |
| Human responsiveness | Receipt and signed decision timestamps | Compute queue and response delays, unresolved cases | Approver independence without identity verification |
| Pause enforcement | Broker receipts and external test results | No mediated forbidden execution while frozen | Hidden routes absent from the broker |
| Tamper evidence | Hash chain plus separately witnessed head/count | `python3 -m agent_delegate.audit results/final` (harness in Git history, `f6bcc6a`) | A locally rewritten chain with rewritten checkpoints |
| Gate coverage | Tool inventory, boundary tests, incident exceptions | Challenge unknown/indirect action routes | Absolute completeness |
| Benign-case cost | Pauses, completion, case counts, sampling frame | Inspect denominators and false alarms | Production prevalence from this toy suite |

Publish event schemas, aggregate counts, capability-change metadata and independently anchored commitments. Keep private worker content, prompts, reasoning, personal identifiers and security details out of public logs. Production commitments need unpredictable salts retained for authorized verification; unsalted hashes of short grievances leak via guessing. This fixture hashes synthetic content and is not a privacy system.

Do not advertise a hash chain as proof that logging was complete. The reference logger refuses to overwrite a run and detects edits relative to retained checkpoints; it is not an OS-enforced append-only store, a signature service or remote attestation.
