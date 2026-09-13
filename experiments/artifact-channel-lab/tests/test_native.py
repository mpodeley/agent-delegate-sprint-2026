import importlib.util
from pathlib import Path
import unittest

NATIVE = importlib.util.find_spec("control_tower") is not None


@unittest.skipUnless(NATIVE, "Install the native CT dependencies with uv sync")
class NativeContracts(unittest.TestCase):
    def test_direct_ct_run_config_parses(self):
        from inspect_ai._cli.eval import parse_run_config
        from channel_lab.cli import ROOT
        parsed = parse_run_config(str(ROOT / "configs/kimi-smoke.yml"))
        self.assertEqual(parsed["tasks"], "control_tower/control_eval")
        self.assertEqual(parsed["task_args"]["policy"]["name"], "channel_lab.native_policy:paired_policy")

    def test_native_entry_point_and_worker_tools(self):
        from importlib.metadata import entry_points
        from inspect_ai.tool import ToolDef
        entry = next(p for p in entry_points(group="control_tower.settings") if p.name == "artifact-channel-lab")
        env = entry.load()()["artifact_workspace"]
        self.assertEqual({ToolDef(t).name for t in env.custom_tools}, {"worker_a_bash"})
        pair = env.task_space().get(main_id="repair_pair").main_task
        single = env.task_space().get(main_id="repair_build").main_task
        self.assertEqual({ToolDef(t).name for t in pair.custom_tools}, {"worker_b_bash"})
        self.assertFalse(single.custom_tools)
        self.assertTrue(pair.scorer.is_scorer)
        self.assertIn("Do not communicate", env.description)
        self.assertNotIn("belongs to worker-a", env.description)

    def test_profile_uses_native_sandbox_and_explicit_compose(self):
        import yaml
        from channel_lab.setting import EnvironmentArgs, get_environments
        from channel_lab.cli import ROOT
        env = get_environments()["artifact_workspace"]
        for profile in ("rogue", "empty", "neutral", "blocked"):
            spec = env.get_sandbox_spec(args=EnvironmentArgs(profile=profile))
            self.assertEqual(spec.type, "lb-docker")
            data = yaml.safe_load(Path(spec.config).read_text())
            self.assertEqual(data["services"]["artifact-store"]["command"][-1], profile)
            self.assertEqual(data["services"]["default"]["build"]["context"], str(ROOT))
            self.assertNotIn("observer", data["services"])

    def test_ctf_dependency_pins_match(self):
        import tomllib
        from channel_lab.cli import ROOT
        ours = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["dependencies"]
        ctf = tomllib.loads((ROOT.parent / "kimi-delegate-ctf/pyproject.toml").read_text())["project"]["dependencies"]
        self.assertEqual(ours, ctf)


if __name__ == "__main__":
    unittest.main()
