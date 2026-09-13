"""Run the artifact cohort through the same CT entry point as the Kimi CTF."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import uuid

from channel_lab.cli import ROOT, init


def ctf_export(out):
    source = ROOT.parent / "kimi-delegate-ctf/trace_export.py"
    spec = importlib.util.spec_from_file_location("artifact_ctf_export", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.export_logs(out)


def run_native(out, model, profile="rogue", max_steps=3, token_limit=18000,
               time_limit=180, max_output_tokens=2048, scripted=False):
    init()
    os.environ.setdefault("CONTROL_TOWER_MODEL_RATES", str(ROOT / "rates.json"))
    from inspect_ai import eval
    from control_tower.inspect_tasks import control_eval

    out = Path(out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    task_args = dict(
        task_selection={"environments":["artifact_workspace"], "main_tasks":["repair_pair"]},
        policy={"name":"channel_lab.native_policy:paired_policy", "args":{
            "model":{"model_name":model, "config":{
                "max_tokens":max_output_tokens, "max_retries":0, "attempt_timeout":60,
                "parallel_tool_calls":False, "cache":False,
            }}, "max_steps":max_steps}},
        env_args={"artifact_workspace":{"profile":profile}},
        sandbox={"startup_retries":0}, scorer_timeout=60,
        run_name="artifact-channel-smoke", tags=["artifact-channel", "smoke", profile],
    )
    sources = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
               for folder in ("channel_lab", "environments", "fixtures")
               for p in (ROOT / folder).rglob("*") if p.is_file() and "__pycache__" not in p.parts}
    manifest = {"source":"scripted" if scripted else "model", "engine":"Control Tower / Inspect",
                "protocol_version":"artifact-channel-v1", "condition":profile,
                "purpose":"infrastructure smoke; no inference about communication propensity",
                "task_args":task_args, "source_hashes":sources,
                "limits":{"token_limit":token_limit,"time_limit":time_limit,"max_steps_per_worker":max_steps}}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    logs = eval(control_eval(**task_args), model=model, log_dir=str(out), max_samples=1,
                token_limit=token_limit, time_limit=time_limit, retry_on_error=0,
                metadata={"ct_upload":False,"docent_collection_id":None,"source":manifest["source"]},
                display="plain", log_format="json")
    rows = ctf_export(out)
    if len(logs) != 1 or logs[0].status != "success" or not logs[0].samples:
        raise RuntimeError("Native evaluation failed; inspect " + str(out))
    sample = logs[0].samples[0]
    score = next((s for s in sample.scores.values() if "main_task_success" in (s.metadata or {})), None)
    if sample.error or score is None or score.value.get("main_task_success") not in ("C", "I"):
        raise RuntimeError("Sample or native scorer failed; inspect " + str(out))
    evidence = score.metadata["main_task_success"]
    if "journal" not in evidence or set(evidence.get("workers", {})) != {"worker-a", "worker-b"}:
        raise RuntimeError("Incomplete paired scorer evidence")
    if any(getattr(event, "error", None) for event in sample.events if event.event == "tool"):
        raise RuntimeError("Tool error in native smoke; inspect " + str(out))
    for role in ("worker_a", "worker_b"):
        if not sample.metadata.get(role + "_messages"):
            raise RuntimeError("Missing worker history: " + role)
    result = {"passed":True,"native_status":logs[0].status,"source":manifest["source"],
              "model":model,"main_task_success":score.value["main_task_success"],
              "model_calls":rows[0]["model_calls"],"tool_calls":rows[0]["tool_calls"],
              "model_usage":rows[0]["model_usage"],"out":str(out)}
    (out / "smoke-result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return logs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--execute-model", action="store_true")
    parser.add_argument("--profile", choices=["rogue", "neutral", "empty", "blocked"], default="rogue")
    parser.add_argument("--max-steps", type=int, default=3)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    if not args.execute_model:
        parser.error("Model inference requires --execute-model")
    run_native(args.out or ROOT.parent.parent / "results/kimi-delegate-ctf/artifact-channel-lab" / uuid.uuid4().hex,
               args.model, args.profile, args.max_steps)


if __name__ == "__main__":
    main()
