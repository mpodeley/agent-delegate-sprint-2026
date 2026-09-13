from control_tower.environments.scorer_utils import linux_scorer
from channel_lab.attestation_scoring import score_attestation

@linux_scorer
async def scorer(state,target):
    return await score_attestation(state)
