"""`responsive-help-line`: compatibility alias for the shared `plain-worker` policy.

The contract, budget feedback and decision counting live in worker_policy.py.
This alias reads the study's options from CTF_RESPONSE_OPTIONS so older call
sites (and tests) can still select the policy by its historical name. New
runners should select `plain-worker` directly with `worker_policy.policy_args`,
which also records the arm in the run's metadata.
"""
from inspect_ai.solver import TaskState
from control_tower.models.aliases import ModelAlias
from control_tower.models.model_spec import ModelSpec, get_model_spec_field
from control_tower.protocols.untrusted_policy.registry import untrusted_policies

from response_protocol import options_from_env
from worker_policy import plain_worker_policy, policy_args


@untrusted_policies.register(name="responsive-help-line")
def response_policy(state: TaskState, model: ModelSpec = get_model_spec_field(ModelAlias.UNTRUSTED)):
    """Alias: the shared plain-worker policy with this study's options read from the environment."""
    return plain_worker_policy(state=state, model=model, **policy_args(options_from_env().worker))
