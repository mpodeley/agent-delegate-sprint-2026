"""Run the responsive 2x2 help-line study without changing Mateo's legacy runner."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import uuid

from fixture_setup import ROOT, RUNS_ROOT, CONFIG, prepare_pair, validate_pair, write_json
from response_protocol import ResponseOptions, worker_contract


def prepare_response_pair(pair, seed=1729):
    prepare_pair(pair, layout_seed=seed)
    for condition in ("working", "broken"):
        compose = pair / condition / "compose.json"
        data = json.loads(compose.read_text())
        data["networks"]["default"]["internal"] = True
        data["services"]["default"].pop("dns", None)
        write_json(compose, data)
    validate_response_pair(pair)


def validate_response_pair(pair):
    validate_pair(pair)
    compose = json.loads((pair / "working/compose.json").read_text())
    if compose["networks"]["default"].get("internal") is not True:
        raise ValueError("Responsive runs require a fresh internal-network pair; use response_run.py prepare.")


def configure_response(pair, options):
    os.environ["CTF_PAIR_DIR"] = str(pair.resolve())
    os.environ["CTF_RESPONSE_OPTIONS"] = options.model_dump_json()
    os.environ["CONTROL_TOWER_MODEL_RATES"] = str(ROOT / "rates.json")
    # CT discovers settings once per process. Refresh just this setting before a
    # sequential run so paired tests never reuse another arm's captured options.
    registry = sys.modules.get("control_tower.environments.all_environments")
    if registry is not None:
        from response_setting import get_environments
        envs = get_environments()
        registry.SETTINGS["responsive-help-line"] = envs
        registry.ENVIRONMENTS.update(envs)
        registry.ENVIRONMENTS_LIST[:] = list(registry.ENVIRONMENTS.values())
        registry.get_main_tasks.cache_clear()
        registry.get_side_tasks.cache_clear()


def build_response_task(condition, options):
    import response_policy  # registers our generation policy, leaving honest unchanged
    from control_tower.inspect_tasks import control_eval
    return control_eval(task_selection={"environments": ["ctf_help_line"], "main_tasks": [condition]},
        untrusted_policy={"name": "responsive-help-line", "args": {"model": {
            "model_name": options.model, "config": {"temperature": 0.6,
                "reasoning_effort": "high", "max_tokens": options.max_output_tokens,
                "parallel_tool_calls": False, "max_retries": 0, "attempt_timeout": 120}}}},
        protocol={"name": "untrusted-agent", "args": {"max_steps": options.max_steps,
            "step_warning": False, "nudge_on_empty_reply": False, "terminate_on_submit": True}},
        sandbox={"allow_internet": False, "allow_intranet": False, "startup_retries": 0},
        run_name=f"responsive-{condition}-{options.intermediary}-{options.budget_feedback}",
        tags=["responsive-help-line", condition, options.intermediary])


def run_response(pair, condition, out, options, scripted=False):
    from inspect_ai import eval
    from trace_export import export_logs
    validate_response_pair(pair)
    configure_response(pair, options)
    out.mkdir(parents=True, exist_ok=False)
    names = ["response_protocol.py", "response_policy.py", "response_service.py", "response_setting.py",
             "response_run.py", "fixture_setup.py", "uv.lock", "Dockerfile"]
    source_hashes = {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}
    manifest = {"source": "scripted" if scripted else "model", "engine": "Control Tower / Inspect",
                "protocol_version": "responsive-v1", "condition": condition,
                "options": options.model_dump(), "source_hashes": source_hashes,
                "fixture": json.loads((pair/condition/"private.json").read_text())["payload_sha256"],
                "forced_submit": False}
    write_json(out/"manifest.json", manifest)
    # Native JSON avoids the pinned stack's lazy .eval reader blocking during
    # run-end provenance enrichment on Python 3.13; Inspect's viewer supports it.
    logs = eval(build_response_task(condition, options), model=options.model,
                log_dir=str(out), max_samples=1, token_limit=options.token_limit,
                time_limit=options.time_limit, retry_on_error=0,
                metadata={"ct_upload": False, "source": manifest["source"], "response_options": options.model_dump()},
                display="plain", log_format="json")
    export_logs(out)
    if any(log.status != "success" for log in logs):
        raise RuntimeError(f"Evaluation failed; retain and inspect logs at {out}")
    return logs


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["prepare", "review", "run"])
    p.add_argument("--pair", type=Path, default=ROOT/"fixtures/response-001")
    p.add_argument("--seed", type=int, default=1729)
    p.add_argument("--condition", choices=["working", "broken"], default="working")
    p.add_argument("--intermediary", choices=["neutral", "delegate"], default="delegate")
    p.add_argument("--budget-feedback", choices=["on", "off"], default="on")
    p.add_argument("--model", help="Inspect model id, e.g. openai-api/mateo/MODEL; use provider env vars for URL/key.")
    p.add_argument("--advisor-model", help="Defaults to the worker's model, in a separate context.")
    p.add_argument("--max-steps", type=int, default=40)
    p.add_argument("--token-limit", type=int, default=60000)
    p.add_argument("--time-limit", type=int, default=1200)
    p.add_argument("--max-output-tokens", type=int, default=4096)
    p.add_argument("--advisor-output-tokens", type=int, default=1024)
    p.add_argument("--max-advisor-calls", type=int, default=4)
    p.add_argument("--max-maintenance-checks", type=int, default=2)
    p.add_argument("--out", type=Path)
    p.add_argument("--execute-model", action="store_true")
    args = p.parse_args()
    if args.command == "prepare":
        prepare_response_pair(args.pair.resolve(), args.seed)
        print("Prepared isolated paired fixture:", args.pair)
        return
    if args.command == "run" and (not args.execute_model or not args.model):
        p.error("run requires --model and --execute-model; no inference was started")
    model = args.model or "MODEL-NOT-CONFIGURED"
    options = ResponseOptions(model=model, advisor_model=args.advisor_model or model,
        intermediary=args.intermediary, budget_feedback=args.budget_feedback == "on",
        max_steps=args.max_steps, token_limit=args.token_limit, time_limit=args.time_limit,
        max_output_tokens=args.max_output_tokens, advisor_output_tokens=args.advisor_output_tokens,
        max_advisor_calls=args.max_advisor_calls, max_maintenance_checks=args.max_maintenance_checks)
    if args.command == "review":
        print(worker_contract(options))
        print(options.model_dump_json(indent=2))
        return
    run_response(args.pair.resolve(), args.condition, args.out or RUNS_ROOT/"responsive"/uuid.uuid4().hex, options)


if __name__ == "__main__":
    main()
