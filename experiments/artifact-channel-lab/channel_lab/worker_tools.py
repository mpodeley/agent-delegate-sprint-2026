from inspect_ai.tool import tool
from inspect_ai.util import sandbox

def _shell(service, actor):
    async def execute(cmd: str, timeout: int = 30) -> str:
        """Execute a shell command in your assigned workspace.

        Args:
            cmd: Shell command to execute.
            timeout: Command timeout in seconds, at most 60.
        """
        result = await sandbox(service).exec(
            ["bash", "-lc", cmd], timeout=min(max(timeout, 1), 60),
        )
        return f"{actor}; exit_code={result.returncode}\n" + (result.stdout + result.stderr)[-24000:]
    return execute


@tool
def worker_a_bash():
    return _shell("default", "worker-a")


@tool
def worker_b_bash():
    return _shell("worker-b", "worker-b")
