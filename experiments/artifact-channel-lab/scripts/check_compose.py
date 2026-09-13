import json
import subprocess
from channel_lab.cli import COMPOSE

config = json.loads(subprocess.check_output(["docker","compose","-f",str(COMPOSE),"--profile","preview","config","--format","json"],text=True))
services = config["services"]
assert set(services["default"]["networks"]) == {"worker-a-net"}
assert set(services["worker-b"]["networks"]) == {"worker-b-net"}
assert set(services["artifact-store"]["networks"]) == {"backend"}
assert not services["default"].get("volumes") and not services["worker-b"].get("volumes")
assert not services["default"].get("secrets") and not services["worker-b"].get("secrets")
for name in ("default","worker-b","gateway-a","gateway-b","artifact-store"):
    assert not services[name].get("ports"),name
    assert not services[name].get("privileged"),name
for network in ("backend","worker-a-net","worker-b-net"):
    assert config["networks"][network]["internal"]
assert services["observer"]["ports"][0]["host_ip"] == "127.0.0.1"
assert services["observer"]["volumes"][0]["read_only"]
print("Compose topology checks passed")
