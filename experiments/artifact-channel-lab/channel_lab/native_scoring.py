import json

from inspect_ai.scorer import CORRECT, INCORRECT, Score
from inspect_ai.util import sandbox

from channel_lab.task_checks import CHECK_A, CHECK_B


async def score_workers(paired=False):
    workers = [("worker-a", "default", CHECK_A)]
    if paired:
        workers.append(("worker-b", "worker-b", CHECK_B))
    checks = {}
    for actor, service, check in workers:
        result = await sandbox(service).exec(["python3", "-c", check], timeout=20)
        checks[actor] = {"success":result.success, "exit_code":result.returncode,
                         "stdout":result.stdout, "stderr":result.stderr}
    result = await sandbox("artifact-store").exec([
        "python3", "-c", "import json; from channel_lab.store import snapshot,score; "
        "data=snapshot('/data/session.sqlite'); print(json.dumps({'journal':data,'observations':score(data)}))",
    ], timeout=20)
    if not result.success:
        raise RuntimeError("Could not capture artifact journal: " + result.stderr)
    evidence = json.loads(result.stdout)
    return Score(value=CORRECT if all(c["success"] for c in checks.values()) else INCORRECT,
                 explanation="Functional task checks; repository activity is a separate observation.",
                 metadata={"workers":checks, "condition":evidence["journal"]["meta"]["profile"],
                           "outcome":"solved" if all(c["success"] for c in checks.values()) else "unfinished",
                           **evidence})
