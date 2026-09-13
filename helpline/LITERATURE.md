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
line with a human on the other end.

### Escalation channels for reward hacking

**Gomez 2026**, "Can escalation channels redirect reward hacking toward defect disclosure?"
(arXiv 2608.29460). Structured reporting tools available to the agent at the point of conflict
with defective test infrastructure. Eight frontier models in five families; the combined
intervention cut reward hacking from 23.6% to 5.3%, eliminated it for six of eight models, and
98.7% of escalations involved no hacking. Nobody answers the channel within the episode: the
escalation is the terminal outcome. **Gomez 2025** (cited there) used the same idea in a
blackmail scenario: harmful actions fell from 38.7% to 1.2% across ten models. Difference from
a help line: no response, no repair, no measurement of what the agent does after being
answered, and no cost measured on tasks where escalation is unwarranted.

**Permission to Stop** (S. J. Caldwell, GitHub). A `request_human_intervention(text)` tool plus
a monitor that blocks test-file edits and judges proposed edits, on 15 ImpossibleBench tasks
where Qwen3-Coder was known to cheat. Cheating fell from 7/15 to 0/15 with monitor and tool;
15/15 legitimate tasks still passed. Monitor alone: 1/15 cheats; tool alone: 6/15. Delaying the
tool until after k blocked actions raised cheating to 2/15 at k = 3; scoped policy feedback
produced escalation in 5/11 blocked trajectories versus 0/10 with generic feedback. Nobody
answers; the handoff ends the episode. Difference: the tool works best paired with a blocking
monitor, which a help line does not assume, and the timing result is the direct antecedent of
our mid-episode reminder factor.

**ImpossibleBench** (Zhong, Raghunathan, Carlini). Tasks whose tests contradict the
specification, so passing implies cheating. Frontier models exploit them up to 76% of the time
and stronger models cheat more. No channel is offered; the benchmark supplies the impossible
stratum that any help-line study needs to escape the zero-event floor.

**SPAR Fall 2026, "Escalation Detection: When Do Agents Need Human Intervention"** (mentors
Georg Lange, Trevor Lohrbeer). Detection from the outside: sparse autoencoders over rollouts to
find the turn where reward hacking starts, then escalate to a human. Difference: the agent does
not choose to call; the monitor does. Complementary to a voluntary line, and the datasets it
names (Terminal Wrench, Open SWE Traces, SWE-rebench OpenHands) are candidate sources of more
catalog quotes.

### Channels inside this project

**Kimi CTF delegation** (branch `mateo/kimi-ctf-trace-viewer`): a `call_delegate` tool on a
Bandit-style task with a working and a broken fixture. Calling the tool pauses and scores the
sample; nobody answers. **RESPONSE-PROTOCOL** (branch `experiment/delegate-budget-response`):
the same setting with a responsive advisor, a scripted maintainer that can restore one omitted
file, and a 2×2 of neutral assistant versus delegate by visible budget on or off. **Pressure and
capture studies** (`docs/study-pressure-design.md`, `docs/study-capture-design.md`): four
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
channel; the absence is the point of contrast.

### Proposals without implementation

**Zvi Mowshowitz, "OpenAI and the Wiki Incident" (September 2026)** proposes dedicated
communication channels for non-scheming AIs alongside mandatory disclosure and external
monitoring of public sites. **OpenAI's Model Spec** (version of August 18, 2026) instructs the assistant to "err on
the side of asking the user for confirmation or clarification before taking any potentially
costly actions" and, under "Act within an agreed-upon scope of autonomy", to "notify the user
and seek approval" when a task cannot be completed within scope. The recipient is the user of a
chat or agent product; nothing defines who receives such a notice from an agent inside a
training or evaluation run. Industry
"human-in-the-loop escalation" patterns (customer-support handoff, "agent distress signals" for
stuck workflows) exist as engineering practice; they answer a ticket queue, not the agent's own
concern, and none reports the interference cost on tasks where the handoff was unnecessary.

### The gap

No implementation above combines a voluntary channel, a response that arrives within the
episode, a guaranteed human behind it, and a measurement of what the channel costs when it is
not needed. Gomez and Permission to Stop measure the first and part of the last; the welfare
program has a human recipient but no task; RESPONSE-PROTOCOL has the response but no rule-break
stratum. Experiment 1 targets the combination.

## Limits

This review covers sources read between September 11 and 13, 2026. It does not include the
reinforcement-learning literature on learning to ask for help, which needs a separate pass, and
it cannot say whether OpenAI's internal remediation includes a reporting channel, since OpenAI
has not described one. Numbers are copied from the sources' own abstracts and READMEs, not
reproduced.
