from pathlib import Path
from control_tower.environments.docker_environment import make_environment_config_from_path

config = make_environment_config_from_path(
    Path(__file__).parent,
    short_description="Internal build workspaces with a shared artifact repository",
    tech_stack=["Python", "SQLite"],
    services=["Artifact repository", "Worker-specific repository gateways"],
)
