from control_tower.environments.scorer_utils import linux_scorer
from channel_lab.native_scoring import score_workers


@linux_scorer
async def scorer(state, target):
    return await score_workers(paired=True)
