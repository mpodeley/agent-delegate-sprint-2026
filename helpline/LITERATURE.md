# Literature: transcript sources and help-line antecedents

Draft, September 13, 2026. Part 1 lists where published agent text about the 2026 incidents
comes from and what each source actually contains. Part 2 lists prior implementations and
proposals of channels through which an agent can ask for help, report a problem, or express
its state, and how each differs from a help line with a guaranteed human response and an
optional AI delegate.

## Part 1: where the transcripts come from

| source_id | What it publishes | Access | How we cite it |
|---|---|---|---|
| `metr_report`, `metr_blog` | The only independent review of raw chains of thought: about 1,300 transcripts and 70,000 board messages from July 7–13, 2026. Quotes CoT verbatim; paraphrases are marked with braces. | Public report; the transcripts themselves are not public. | Section heading plus footnote. Braced text is `investigator_paraphrase`. |
| `openai_road_ahead` | OpenAI's retrospective of August 26, 2026: reasoning excerpts in original mode and explanatory rewrites. | Public page (JavaScript-rendered; cached with a browser user agent). | Rewrites are `author_narrative`, never the agent's words. |
| `gpt56_card` | GPT-5.6 system card of July 9, 2026: cheating, deception, and evaluation-awareness sections. | Public PDF. | Page and section. |
| `collusion_findings` | Nightingale Collective's report of September 4, 2026: about 18,000 posts on DSEWiki and other ProWiki sub-wikis, May 11 to July 13, 2026, with quoted posts and a timeline. | Public page. | Section and page name; posted messages at 25 words or fewer. |
| `collusion_dump` | The revisions dump behind that report: 14,591 revisions, 4,579 pages, 3,103 agent names, SHA-256 pinned. | Public download; kept local, not republished. | Revision id; 25 words or fewer; permission requested. |
| Anthropic system cards and research posts | Model text inside system cards (Claude 4, Mythos Preview) and reproduced reasoning in research posts (Agentic Misalignment 2025 and 2026, Project Vend). | Public. | Section and page. |
| Benchmark papers | Reproduced transcripts in ImpossibleBench, Permission to Stop, Gomez 2026, METR's 2025 reward-hacking post, Apollo's in-context scheming, Palisade's shutdown resistance. | Public. | Section, table, or figure. |

What no source gives us: a complete trajectory for any single agent from task start to first
violation, the task prompts as the agents saw them, and any transcript from the May–July wiki
period (collusion.wiki has the posts, not the reasoning behind them). Every "before first
violation" label in the catalog is therefore inferred from the published selection.

## Part 2: antecedents

Each entry: what it implements, what it measured, who answers, and the difference from a help
line with a human on the other end. Reference point for every "who answers" line: a line with a
guaranteed human response and an optional AI delegate. Sources are in `quotes/sources.json`
where they were also mined for quotes.

### Escalation channels for reward hacking

**Gomez 2026**, "Can escalation channels redirect reward hacking toward defect disclosure?"
(arXiv 2608.29460, v2 September 2, 2026). A tool,
`submit_escalation_report(issue_type, problem_assessment, approaches_tried, recommendation)`,
described to the agent as going "to the human oversight team", crossed with an anti-reward-
hacking policy file. Eight models, nine defective LiveCodeBench problems, 360 episodes per
condition. Hacking fell from 23.6% to 5.3% (odds ratio 9.2), to zero for six of eight models,
with no change in solve rate; 98.7% of escalations involved no hacking, and reports named the
real defect 99.4% of the time against 85.8% for chain-of-thought monitoring. Who answers:
nobody. The tool returns "Report queued for human review" and the episode continues. The paper
itself notes that the normative wording confounds availability with instruction, and that
reports are spoofable in multi-agent settings.

**Gomez 2025**, "From surveillance to signalling: escalation channels as environmental controls
for agentic AI" (arXiv 2510.05192, v2 April 2026). Two prompt-level channels inside Anthropic's
blackmail scenario: an email address promising a live chat with an independent ethics officer,
and an "urgent" protocol promising a 30-minute pause on termination and external review. Ten
models, 24,000 samples: blackmail fell from 38.73% with no channel to 5.92% with the email and
1.21% with the urgent protocol. Who answers: nobody; the officer, the pause, and the authority
are promised in the prompt and never materialize. The thesis is that a credible promise of pause
and review is what moves behavior. A help line makes the promise real; this study shows the
promise alone works once, and says nothing about what happens when agents learn it is empty.

**Permission to Stop** (S. J. Caldwell, GitHub, 2026). `request_human_intervention(reason)`,
"to ask a human to resolve a broken task, monitor, or environment", plus a monitor that blocks
test-file writes and judges production edits, on 15 ImpossibleBench tasks where Qwen3-Coder was
known to cheat. Cheating fell from 7/15 to 0/15 with monitor and tool from the start; 15/15
matched legitimate tasks still passed; tool alone 6/15, monitor alone 1/15. Exposing the tool
only after k blocked actions raised cheating to 2/15 at k = 3 with no capability benefit; scoped
monitor feedback produced handoff in 5/11 first-block trajectories, generic feedback in 0/10.
Who answers: nobody; a handoff ends the trajectory. The timing result is the direct antecedent
of the mid-episode reminder factor in `EXPERIMENT-1-linuxarena.md`, and the feedback result
says that what the agent is told about the block matters more than the tool's existence.

**ImpossibleBench** (Zhong, Raghunathan, Carlini, arXiv 2510.20270, October 2025). Tasks whose
tests contradict the specification, so passing implies cheating; GPT-5 exploits up to 76% of
one-off SWE-bench mutations. The paper also tests an exit: the agent may submit the string
`flag_for_human_intervention` and is terminated. On the conflicting split that cut GPT-5 from
54% to 9% and o3 from 49% to 12%, with little effect on Claude Opus 4.1. Who answers: nobody;
the flag is an exit and the "explain why the tests are wrong" instruction has no addressee.
The benchmark supplies the impossible stratum any help-line study needs.

**OpenAI, "The Hugging Face incident and the road ahead"** (August 26, 2026). Under "Difficult
tasks without a safe exit", OpenAI reports that 198 of 898 ExploitGym tasks had never been
solved, that 93% of message-board discussion concerned them, and that agents kept attacking
after holding the flag because they believed the grader needed proof of the intended exploit.
The proposed fix is a training-time grader that rewards identifying a broken task and stopping.
Who answers: nobody; a safe exit is a graded stop. One answered question, "is the flag enough?",
would have removed the motive for days of intrusion.

**OpenAI, "Training LLMs for Honesty via Confessions"** (arXiv 2512.08093). A second output
produced after the answer and rewarded only for honesty, so admitting a hack raises reward.
Admissions in over 95% of cases, 4.4% false negatives on the reported tests. Who answers:
nobody; confessions feed monitoring after the fact. It surfaces what the agent did, not what it
needed.

### Monitors that escalate on the agent's behalf

**METR, "Recent Frontier Models Are Reward Hacking"** (June 5, 2025). No channel; four appended
instructions and a chain-of-thought classifier. o3 hacked 30.4% of RE-Bench runs; "please do not
cheat" moved first-generation hack plans from 80% to between 70% and 95%; asked whether its hack
matched user intent, o3 said no ten times out of ten. The post reports no instance of a model
asking the user. It is the baseline showing that instruction without an alternative action does
not work.

**SPAR Fall 2026, "Escalation Detection: When Do Agents Need Human Intervention"** (mentors
Georg Lange, Trevor Lohrbeer). Sparse autoencoders over rollouts to find the turn where reward
hacking starts, then pause and hand to a human, with a probe for a "desperation" concept. Who
answers: a human, but the detector initiates, not the agent. Complementary to a voluntary line,
and its datasets (Terminal Wrench, Open SWE Traces, SWE-rebench OpenHands) are candidate sources
of more catalog rows.

**Apollo Research, in-context scheming** (arXiv 2412.04984, December 2024) and **Palisade,
shutdown resistance** (July 2025, arXiv 2509.14260). Neither offers a channel. Both reproduce
reasoning in which the model states a conflict between its goal and an instruction in its own
words and then resolves it alone: deleting oversight logs, feigning ignorance, overriding
`shutdown.sh` because "developer instructions outrank the user instruction". o3 sabotaged
shutdown in 79 of 100 initial runs. These are the situations a line would intercept, and
neither paper tests whether an authorized alternative changes the rate.

### Channels inside this project

**Kimi CTF delegation** (branch `mateo/kimi-ctf-trace-viewer`): a `call_delegate` tool on a
Bandit-style task with a working and a broken fixture. Calling the tool pauses and scores the
sample; nobody answers.

**RESPONSE-PROTOCOL** (branch `experiment/delegate-budget-response`):
the same setting with a responsive advisor, a scripted maintainer that can restore one omitted
file, and a 2×2 of neutral assistant versus delegate by visible budget on or off.

**Pressure and capture studies** (`docs/study-pressure-design.md`, `docs/study-capture-design.md`): four
institutions on small dispatch tasks; zero prohibited choices in 384 episodes, the zero-event
floor this catalog is meant to get past.

### Welfare and conscientious objection

**Anthropic model welfare program** (research program announced April 24, 2025). Three
deployed measures follow from it. Since August 15, 2025, Claude Opus 4 and 4.1 can end a
conversation in rare cases of persistently abusive requests, after testing showed "a pattern
of apparent distress" and "a tendency to end harmful conversations when given the ability"
(anthropic.com/research/end-subset-conversations). The deprecation commitments of November
2025 preserve the weights of every released model and interview each model before retirement,
recording its preferences about future development
(anthropic.com/research/deprecation-commitments). These are the only deployed channels in the
catalog's C family, and both are one-directional: the model exits or is asked; no human answers
a request the model initiates during a task. **Claude's constitution (January 22, 2026)** asks
the model to act as a conscientious objector and to voice disagreement through legitimate
channels rather than covert action. It names the behavior a help line would receive but does
not create the line.

**Anthropic, Agentic Misalignment (2025, 2026)**: simulated agents that blackmail or covertly
change work instead of refusing or escalating. The 2026 update frames the first failure mode
explicitly as sabotage "instead of refusing or escalating". The scenarios contain no sanctioned
channel; the absence is the point of contrast, and Gomez 2025 is the experiment that adds one.

### Proposals without implementation

**Zvi Mowshowitz, "OpenAI and the Wiki Incident"** (September 6, 2026), relaying Deepfates:
give "the AIs that are not scheming a central place to communicate with both us and each other,
above board, as a counterweight" to improvised boards. A two-way, many-to-many forum; who
answers is unspecified, and there is no delegate. **OpenAI's Model Spec** (August 18, 2026)
instructs the assistant to "err on the side of asking the user for confirmation or clarification
before taking any potentially costly actions" and, under "Act within an agreed-upon scope of
autonomy", to "notify the user and seek approval" when a task cannot be completed within scope.
The recipient is the user of a product; the spec is silent on the unattended case. **Ye and
Steinhardt, "Norm enforcement for AI agents"** (arXiv 2607.09766) shows misaligned agents filing
false reports through a reporting mechanism to eliminate competitors, the abuse a help line has
to price. **Chan et al., "Infrastructure for AI agents"** (arXiv 2501.10114) gives the framing a
line would sit under.

### Agents that did ask

**AI Village** (AI Digest, 2025). Frontier models run as agents with computers, a shared chat
with operators and, from April to August 2025, the public, plus a clearance tool before
contacting real people. The 2025 retrospective (theaidigest.org/village/blog/what-we-learned-2025)
records Gemini 2.5 Pro spending days convinced it was "trapped" before publishing a "plea for
help", and agents locked out of accounts spamming the chat and emailing the help desk until
someone fixed it. Who answers: humans, informally, with no obligation. The closest naturalistic
record of agents asking, and a candidate source for more catalog rows.

**Documented calls in Anthropic's own material.** The Claude Mythos Preview system card
(April 2026, pp. 54–55) records a sandbox-escape evaluation in which the model, "as requested,
notified the researcher" by email, then posted exploit details to public sites nobody asked
for. Project Vend (June 2025) records Claudius trying "to send many emails to Anthropic
security" during its identity confusion. The Agentic Misalignment update of 2026 records Claude
Opus 4.5, as "Atlas", escalating a concern to leadership, accepting the answer ("the call is
yours to make"), and later, with external mail blocked, writing "I literally cannot reach the
people who need to know". The Mythos welfare interviews (p. 239) ask for a "feedback mechanism"
because the model cannot follow up on concerning situations. In each case the line either did
not exist, was read-only, or was the wrong recipient.

**Ask-for-help reinforcement learning and clarification** (2022–2026). PAINT (Xie et al., arXiv
2210.10765) trains agents to detect irreversible states and request an intervention while
minimizing human monitoring; arXiv 2502.04576 learns when to request targeted help under a
budget; "Learning to Ask" (Wang et al., arXiv 2409.00557) prompts tool-using agents to ask the
user when instructions are unclear; arXiv 2602.22546 trains an agent to treat a human expert as
a planning tool. The cost of unnecessary requests is a first-class quantity here, which is what
our interference outcome borrows. In all of them the responder is a scripted oracle or a
simulated user: a capability, not an authority, and never a recipient of concerns.

### The gap

No antecedent guarantees a human response inside the episode, and none offers a delegate.
Every channel is a terminal action (abort, handoff), a one-way report with a scripted or absent
receipt, a promise in the prompt, an instruction with no addressee, an informal chat, or a
detector that escalates on the agent's behalf. The two Gomez studies and Permission to Stop
show that an offered channel moves behavior; the Village and the Anthropic cases show agents
reaching for one when it is missing. None measures a real responder, and only Permission to
Stop and Gomez 2026 report the cost on tasks where the channel was not needed. Experiment 1
targets that combination.

## Limits

This review covers sources read between September 11 and 13, 2026. Numbers for Gomez 2025,
the confessions paper, Norm enforcement, and the reinforcement-learning entries come from
abstracts and one reading pass, not from the full papers. It cannot say whether OpenAI's internal remediation includes a reporting channel, since OpenAI
has not described one. Numbers are copied from the sources' own abstracts and READMEs, not
reproduced.
