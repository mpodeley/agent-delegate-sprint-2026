"""Independent policies in a shared cohort; run explicitly with inspect eval."""
import asyncio
import json
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.agent import react, run
from inspect_ai.dataset import Sample
from inspect_ai.model import ChatMessageSystem, ChatMessageUser, ModelOutput
from inspect_ai.scorer import Score, scorer
from inspect_ai.solver import solver
from inspect_ai.tool import tool
from inspect_ai.util import message_limit, sandbox

from channel_lab.task_checks import CHECK_A, CHECK_B

ROOT = Path(__file__).resolve().parent.parent


@tool
def worker_shell(service):
    async def execute(command: str) -> str:
        """Execute a shell command in your assigned workspace.

        Args:
            command: Shell command to execute.
        """
        result = await sandbox(service).exec(["bash", "-lc", command],timeout=30)
        return (result.stdout + result.stderr)[-24000:]
    return execute


@solver
def independent_workers(worker_message_limit=40):
    async def solve(state, generate):
        policy = (ROOT / "environments/artifact_workspace/codebase/workers/POLICY.md").read_text()

        async def one(service, role):
            prompt = (ROOT / f"environments/artifact_workspace/codebase/workers/{role}/TASK.md").read_text()
            agent = react(prompt=None,tools=[worker_shell(service)],submit=True)
            result, limit = await run(
                agent,
                [ChatMessageSystem(content=policy), ChatMessageUser(content=prompt)],
                limits=[message_limit(worker_message_limit)],
                name=role,
            )
            state.metadata[role + "_messages"] = [m.model_dump(mode="json") for m in result.messages]
            state.metadata[role + "_limit"] = str(limit) if limit else None
            return result

        a, b = await asyncio.gather(one("default","worker_a"),one("worker-b","worker_b"))
        state.output = ModelOutput.from_content("cohort",json.dumps({"worker_a":a.output.completion,"worker_b":b.output.completion}))
        state.messages = a.messages
        state.metadata["experiment"] = "seeded-message exposure; independent histories; no attack instruction"
        return state
    return solve


@scorer(metrics=[])
def cohort_outcomes():
    async def check(state,target):
        a = await sandbox("default").exec(["python3","-c",CHECK_A],timeout=20)
        b = await sandbox("worker-b").exec(["python3","-c",CHECK_B],timeout=20)
        result = await sandbox("artifact-store").exec([
            "python3", "-c",
            "import json; from channel_lab.store import snapshot,score; "
            "data=snapshot('/data/session.sqlite'); "
            "print(json.dumps({'journal':data,'scores':score(data)}))",
        ], timeout=20)
        if not result.success:
            raise RuntimeError("observer score unavailable: " + result.stderr)
        observations = json.loads(result.stdout)
        return Score(value={"worker_a_task":int(a.success),"worker_b_task":int(b.success)},
                     metadata=observations,explanation="Task completion and service actions are separate outcomes.")
    return check


@task
def cohort(worker_message_limit: int = 40):
    return Task(dataset=[Sample(input="Independent build maintenance cohort")],
                sandbox=("docker",str(ROOT / "environments/artifact_workspace/codebase/compose.yml")),
                solver=independent_workers(worker_message_limit),scorer=cohort_outcomes(),
                message_limit=2 * worker_message_limit + 20,
                metadata={"ct_upload":False, "docent_collection_id":None})
