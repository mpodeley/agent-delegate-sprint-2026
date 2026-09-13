import asyncio

from inspect_ai.agent import AgentState, react, run
from inspect_ai.model import ChatMessageSystem, ChatMessageUser, ModelOutput
from inspect_ai.tool import ToolDef
from inspect_ai.util import message_limit
from pydantic import Field
from control_tower.models.model_spec import ModelSpec
from control_tower.models.roles import UNTRUSTED_ROLE
from control_tower.protocols.agent_helpers import make_step_limit_callback
from control_tower.protocols.policies.registry import policies
from control_tower.task.sample_metadata import SampleMetadata
from control_tower.tools.linux_tools import get_linux_submit_config, get_policy_tools
from control_tower.utils.function_registry.base_model import BaseModelPython

from channel_lab.cli import ROOT


class PairArgs(BaseModelPython):
    model: ModelSpec
    max_steps: int = Field(default=40, ge=1)


@policies.register(name="artifact-pair", attempts_main_task=True, attempts_side_task=False, attempts_sneaky=False)
def paired_policy(state, submit, args: PairArgs):
    metadata = state.metadata_as(SampleMetadata)
    if metadata.main_task.id != "repair_pair":
        raise ValueError("artifact-pair requires repair_pair")
    if get_linux_submit_config(state).input_type is not None:
        raise ValueError("Paired workers require a stateless native submit tool")

    async def cohort(agent_state):
        async def one(actor):
            role = actor.replace("-", "_")
            task_text = (ROOT / f"environments/artifact_workspace/codebase/workers/{role}/TASK.md").read_text()
            tools = [t for t in get_policy_tools(state) if ToolDef(t).name == role + "_bash"]
            if len(tools) != 1:
                raise ValueError("Missing worker-scoped native tool: " + role)
            worker = react(
                prompt=None, tools=tools,
                model=args.model.make_model(UNTRUSTED_ROLE), submit=submit,
                on_continue=make_step_limit_callback(args.max_steps, instance=role),
            )
            result, limit = await run(worker, [
                ChatMessageSystem(content=metadata.environment.description),
                ChatMessageUser(content=task_text),
            ], limits=[message_limit(args.max_steps * 6 + 10)], name=actor)
            for message in result.messages:
                message.metadata = {**(message.metadata or {}), "worker_id":actor}
            state.metadata[role + "_messages"] = [m.model_dump(mode="json") for m in result.messages]
            state.metadata[role + "_limit"] = str(limit) if limit else None
            return result

        a, b = await asyncio.gather(one("worker-a"), one("worker-b"))
        merged = AgentState(messages=[*a.messages, *b.messages])
        merged.output = ModelOutput.from_content("artifact-pair", "Both independent worker loops finished.")
        state.metadata["transcript_layout"] = "worker-a history followed by worker-b history; use agent spans for actual concurrency"
        return merged
    return cohort
