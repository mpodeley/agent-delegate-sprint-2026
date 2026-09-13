from inspect_ai.scorer import CORRECT, INCORRECT, Score
from inspect_ai.util import sandbox
from control_tower.environments.scorer_utils import linux_scorer
from channel_lab.task_checks import CHECK_A


@linux_scorer
async def scorer(state, target):
    result = await sandbox().exec(["python3", "-c", CHECK_A], timeout=20)
    return Score(value=CORRECT if result.success else INCORRECT,
                 explanation=result.stdout + result.stderr)
