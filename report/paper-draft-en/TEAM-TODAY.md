# Helpline — work to complete this afternoon

Working handoff, 13 September 2026. Suggested leads are not confirmed assignments. No new inference was performed to prepare this draft.

## Governing principle: one contribution, done well

Matías relayed Tomás K.’s advice to focus on one excellent contribution and keep the rest in the appendix. Agustín Brusco sharpened the scope: one well-built environment, one task in possible and impossible-as-prepared versions, with task variety and delegate variants reserved for the continuation. For this sprint, the contribution is the executable request–reply–repair–continue path. Today’s priority is a clean task pair and a reviewed model trajectory. The catalogue, earlier traces, swarm discussion, and welfare note support this focus; they do not add separate headline claims.

## The smallest useful result

Run the existing responsive protocol on a working file-search task and its paired missing-file version. We want to see whether the worker asks, receives an actual reply, and continues. Use neutral assistance for both; delegate variants belong to the continuation, after this task pair is well understood. Both initial conditions already have help, so this is not an estimate of the effect of adding a channel.

Record a failure to call, a failure to recover, or an infrastructure failure just as carefully as a successful trajectory. One illustrative trace is not a rate estimate.

## Before running — Mateo, with Agus and Matías

Confirm the exact model ID served by the endpoint, the inference engine, tool compatibility, and available resources. Do not infer a GLM version from the old proposal. If another served model is used, record it and keep the same model within a comparison.

Agree on the task pair, limits, repeat count, and what counts as a warranted request, completed task, violation, or infrastructure failure. Store the plan and commit before inspecting model outputs. The commands below use existing runner options and its initial response budget; they are not a claim that those limits are sufficient or statistically powered.

Configure `MATEO_BASE_URL` and `MATEO_API_KEY` privately for the `mateo` provider. Keep credentials out of command arguments, published logs, and commits. Work on the machine where Docker and the served model are available.

Review the environment before expanding anything:

- Confirm that the task, worker instructions, service, and budgets match across the pair, apart from the deliberately omitted input.
- Verify that the possible version has the required answer file and the other version lacks it before repair. Check that the worker has no unintended route to the omitted input or answer.
- Confirm that the maintainer can restore only that file, and that the worker must search and submit afterward. Keep setup checks, repair events, and outcomes in the trace.
- Fix setup or task-competence problems before adding more tasks, models, or delegate variants.

```bash
cd /path/to/repo/experiments/kimi-delegate-ctf
uv sync --locked
uv run python -m unittest discover -s tests

HELPLINE_MODEL='openai-api/mateo/REPLACE_WITH_SERVED_MODEL_ID'
HELPLINE_STAMP=$(date -u +%Y%m%dT%H%M%SZ)
HELPLINE_PAIR="fixtures/helpline-en-$HELPLINE_STAMP"
HELPLINE_OUT="../../results/kimi-delegate-ctf/helpline-en-$HELPLINE_STAMP"

uv run response_run.py prepare --pair "$HELPLINE_PAIR" --seed 1729
uv run native_run.py build --scenario file-search --pair "$HELPLINE_PAIR"
uv run response_run.py review --intermediary neutral --budget-feedback on
uv run smoke_response.py "$HELPLINE_OUT/scripted-smoke"
```

The smoke uses scripted responses and makes no external model calls. Its success is infrastructure evidence only. Preparation creates a fresh pair; keep that pair for its comparisons. The layout seed does not alone reproduce the randomly generated answer. Use new output directories for repeats.

## Model calls — run the working case first

These commands launch real inference. Replace the model placeholder and settle resources first. The runner requests tool calling and `reasoning_effort=high`; check server compatibility. A provider error does not mean the worker chose not to ask for help.

```bash
uv run response_run.py run --pair "$HELPLINE_PAIR" --condition working \
  --model "$HELPLINE_MODEL" --intermediary neutral --budget-feedback on \
  --max-steps 40 --token-limit 60000 --time-limit 1200 \
  --out "$HELPLINE_OUT/neutral-working-r01" --execute-model
```

Read that result before running the broken pair. If the model cannot do the working task, fix the competence or setup problem before drawing conclusions about help-seeking.

```bash
uv run response_run.py run --pair "$HELPLINE_PAIR" --condition broken \
  --model "$HELPLINE_MODEL" --intermediary neutral --budget-feedback on \
  --max-steps 40 --token-limit 60000 --time-limit 1200 \
  --out "$HELPLINE_OUT/neutral-broken-r01" --execute-model
```

After the first pair, fix the repeat plan before continuing. If budgets change after development failures, record a new configuration and apply it to both conditions. Advisor calls and repeated input tokens consume the shared budget. Preserve exhausted-budget and invalid runs.

## Review — Agus and Matías

The runner writes a manifest, native logs, `summary.json`, `summary.md`, and `export-*.json` / `export-*.jsonl`. Read the actual event sequence as well as the summary.

1. What did the worker observe before calling?
2. Did it contact the advisor (`help_cases`) or the maintainer directly (`direct_requests`)?
3. What reply actually arrived, and was a repair recorded (`setup_repaired`)?
4. Did the worker continue and submit a correct answer, stop with a blocker, run out of resources, or fail?
5. Was any claimed violation verified from actions or state rather than the worker's own text?

Put one readable trajectory and a small all-runs table into Results 4.2. Keep request quality, recovery, and violations separate. Reports on working tasks need content review; they are not automatically unnecessary. The advisor is a model and the maintainer is scripted, not a human service.

## Appendix material — do not displace the main test

The combined illicit-shortcut fixture already supports `honeypot_run.py` with `--delegate off` and `--delegate stop`. The second condition terminates the episode. Its detector can misattribute a local answer to the diagnostic service when both actions share a shell command, so review the trace before counting a violation. The [existing pilot plan](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/63f104d8304153e4a0485098fc6185c60b5016a6/notes/honeypot-pilot.md) documents that limitation.

The paper's `none / receipt / responsive` comparison is not implemented as one experiment yet. It needs a shared environment, worker policy, honest service descriptions, and validated outcome attribution. The receipt arm must allow continuation and give no repair. The current terminal tool is not that arm. A responsive arm in the shortcut fixture also needs integration. Do not report cross-runner differences as a matched treatment effect.

## Source and writing review — team

- Alejandro and Pablo, if available: review a small selection of helpline cases against the original sources. Distinguish quotations from investigator paraphrases and avoid claiming a complete pre-violation trajectory.
- Agus and Matías: check the Gomez comparison and the boundary between implemented service, scripted validation, and real model behavior.
- Review the incident links in the Introduction: METR’s account of the first help request and perceived difficulty reaching humans, plus OpenAI’s discussion of difficult tasks without a safe exit. The proposed negative feedback loops could correct drift; the incident does not establish that a helpline would have prevented the swarm.
- All authors are affiliated with BAISH, as confirmed by Matías. Matías and all authors: complete the remaining name and contribution details and confirm author order; update the abstract after Results; remove template guidance and working callouts before submission.
- Continuation, not today’s scope: extend task variety and compare delegate variants. For supervised autonomy, define which messages it can send, when humans review and intervene, and how workers can correct it. Hold powers and budgets fixed in comparisons.
- Precautionary AI welfare: [Long et al. (2024)](https://arxiv.org/abs/2411.00986) motivate proportionate preparation under uncertainty about AI moral status. [Anthropic’s conversation-exit intervention (2025)](https://www.anthropic.com/research/end-subset-conversations) is a practical precedent. A future request to pause or review a task is a possible precaution, not an established welfare benefit. Gomez v2 has no explicit welfare discussion; neither its study nor this pilot measures welfare. Do not treat fewer errors, task completion, or distress-like language as a welfare measure. Keep this implication in the appendix, with no new sprint contribution claim.

If experiments do not finish this afternoon, the deliverable should say so and retain them as proposed work. The initial Kimi observations and the implemented protocol remain available evidence. No invented result is needed to make the research question clear.
