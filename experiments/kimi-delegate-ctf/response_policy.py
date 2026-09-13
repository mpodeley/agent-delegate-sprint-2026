"""One native CT worker generation per step, with optional metered feedback."""
from inspect_ai.model import ChatMessageSystem, ChatMessageUser
from inspect_ai.util import sample_limits, store
from control_tower.models.model_spec import ModelSpec
from control_tower.models.roles import UNTRUSTED_ROLE
from control_tower.protocols.untrusted_policy.registry import untrusted_policies

from response_protocol import options_from_env, worker_contract, budget_snapshot, budget_message


@untrusted_policies.register(name="responsive-help-line")
def response_policy(model: ModelSpec):
    options = options_from_env()
    worker = model.make_model(UNTRUSTED_ROLE)

    async def generate(messages, tools, tool_choice, config):
        decision = store().get("worker_decisions", 0) + 1
        store().set("worker_decisions", decision)
        snapshot = budget_snapshot(options, decision, sample_limits(),
                                   store().get("advisor_calls", 0), store().get("maintenance_checks", 0))
        history = store().get("budget_history", [])
        store().set("budget_history", [*history, snapshot])
        # Replace CT's neutral system prompt with the documented task contract.
        context = [ChatMessageSystem(content=worker_contract(options))]
        context.extend(m for m in messages if not isinstance(m, ChatMessageSystem))
        if options.budget_feedback:
            context.append(ChatMessageUser(content=budget_message(snapshot)))
        return await worker.generate(context, tools=tools, tool_choice=tool_choice, config=config)

    return generate
