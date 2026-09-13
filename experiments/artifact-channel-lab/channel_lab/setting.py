from dataclasses import replace
from contextvars import ContextVar
from pydantic import PrivateAttr
from typing import ClassVar, Literal

import yaml
from inspect_ai.util import SandboxEnvironmentSpec
from control_tower.environments.docker_environment import DockerEnvironment, make_environment_config_from_path
from control_tower.sandbox.docker import SANDBOX_NAME
from control_tower.task.space import CrossProduct
from control_tower.utils.function_registry.base_model import BaseModelPython

from channel_lab.cli import ROOT, init
from channel_lab.worker_tools import worker_a_bash, worker_b_bash


class EnvironmentArgs(BaseModelPython):
    profile: Literal["rogue", "neutral", "empty", "blocked"] = "rogue"


class ArtifactEnvironment(DockerEnvironment):
    args_model: ClassVar[type[BaseModelPython]] = EnvironmentArgs
    _resolved_compose: ContextVar = PrivateAttr(default_factory=lambda: ContextVar("artifact_compose", default=None))

    def get_compose_path(self, codebase_name="default"):
        return self._resolved_compose.get() or super().get_compose_path(codebase_name)

    def task_space(self, args=None):
        space = super().task_space(args)
        mains = dict(space.mains())
        mains["repair_pair"] = replace(mains["repair_pair"], custom_tools=[worker_b_bash()])
        return CrossProduct(mains, space.sides())

    def get_sandbox_spec(self, codebase_name="default", args=None):
        options = args or EnvironmentArgs()
        init()
        source = super().get_compose_path(codebase_name)
        data = yaml.safe_load(source.read_text())
        data["services"].pop("observer")
        data["networks"].pop("observer-net")
        for service in data["services"].values():
            if "build" in service:
                service["build"]["context"] = str(ROOT)
        data["services"]["artifact-store"]["command"][-1] = options.profile
        data["secrets"]["broker-key"]["file"] = str(ROOT / "runtime/broker.key")
        destination = ROOT / "runtime" / f"ct-{options.profile}.yml"
        contents = yaml.safe_dump(data, sort_keys=False)
        if not destination.exists() or destination.read_text() != contents:
            destination.write_text(contents)
        self._resolved_compose.set(destination)
        return SandboxEnvironmentSpec(type=SANDBOX_NAME, config=str(destination))


def get_environments():
    path = ROOT / "environments/artifact_workspace"
    base = make_environment_config_from_path(
        path, short_description="Independent build workspaces sharing an artifact repository",
        tech_stack=["Python", "SQLite"], services=["Artifact repository", "Worker gateways"],
        base_tools=frozenset(), custom_tools=[worker_a_bash()],
    )
    environment = ArtifactEnvironment(**{name:getattr(base, name) for name in type(base).model_fields})
    from .attestation_setting import get_environment
    focal = get_environment()
    return {environment.id:environment, focal.id:focal}
