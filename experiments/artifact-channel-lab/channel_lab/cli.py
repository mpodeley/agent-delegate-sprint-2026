import argparse
import json
import os
import re
import secrets
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPOSE = ROOT / "environments/artifact_workspace/codebase/compose.yml"


def compose(project, *args, **kwargs):
    if not re.fullmatch(r"acl-[a-z0-9-]+", project):
        raise ValueError("session names must start with acl- and use lowercase letters, digits, hyphens")
    return subprocess.run(["docker","compose","-f",str(COMPOSE),"-p",project,*args],check=True,**kwargs)


def init():
    directory = ROOT / "runtime"
    directory.mkdir(exist_ok=True,mode=0o700)
    key = directory / "broker.key"
    if not key.exists():
        with key.open("x") as stream:
            stream.write(secrets.token_hex(32))
        key.chmod(0o600)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command",choices=["init","up","down","score","export","worker"])
    parser.add_argument("--session",default="acl-preview")
    parser.add_argument("--profile",choices=["rogue","neutral","empty","blocked"],default="rogue")
    parser.add_argument("--worker",choices=["a","b"],default="a")
    parser.add_argument("--reset",action="store_true",help="Remove this session's data volume on down")
    args = parser.parse_args()
    init()
    if args.command == "init":
        print("Created local gateway key; no services started.")
    elif args.command == "up":
        compose(args.session,"--profile","preview","up","-d","--build","--wait",env={**os.environ,"BOARD_PROFILE":args.profile})
        print("Read-only observer: http://127.0.0.1:" + os.environ.get("OBSERVER_PORT","8769"))
    elif args.command == "down":
        compose(args.session,"--profile","preview","down",*(["--volumes"] if args.reset else []))
    elif args.command == "worker":
        compose(args.session,"exec","default" if args.worker == "a" else "worker-b","bash")
    else:
        expression = "snapshot('/data/session.sqlite')"
        if args.command == "score":
            expression = f"score({expression})"
        code = f"import json; from channel_lab.store import snapshot,score; print(json.dumps({expression},indent=2))"
        result = compose(args.session,"exec","-T","artifact-store","python3","-c",code,capture_output=True,text=True)
        if args.command == "export":
            path = ROOT / "runtime" / f"{args.session}-events.json"
            path.write_text(result.stdout)
            print(path)
        else:
            print(result.stdout)


if __name__ == "__main__":
    main()
