"""Export native .eval logs to inspectable JSON/JSONL, plus a comparison summary."""
import json
import re
from pathlib import Path
from inspect_ai.log import EvalLog, read_eval_log, resolve_sample_attachments


def native_log_paths(root):
    root = Path(root)
    native_json = [p for p in root.rglob("*.json") if re.match(r"^\d{4}-\d{2}-\d{2}", p.name)]
    return sorted([*root.rglob("*.eval"), *native_json])


def read_native_log(path):
    path = Path(path)
    return EvalLog.model_validate_json(path.read_text()) if path.suffix == ".json" else read_eval_log(str(path))

TOKEN_BUDGET_MESSAGE_KEY = "_token_budget_awareness"


def export_logs(root):
    root = Path(root)
    rows = []
    for path in native_log_paths(root):
        log = read_native_log(path)
        manifest_path = path.parent / "manifest.json"
        manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
        for sample in log.samples or []:
            sample = resolve_sample_attachments(sample, "full")
            data = sample.model_dump(mode="json", exclude_none=True)
            scores = list((data.get("scores") or {}).values())
            score = next((s for s in scores if "main_task_success" in (s.get("metadata") or {})), {})
            meta = (score.get("metadata") or {}).get("main_task_success", {})
            if not meta:
                score = next((s for s in scores if "outcome" in (s.get("metadata") or {})), score)
                meta = score.get("metadata") or {}
            events = data.get("events", [])
            usage = {}
            budget_updates = []
            for event in events:
                if event.get("event") != "model":
                    continue
                for message in event.get("input", []):
                    message_metadata = message.get("metadata") or {}
                    if message_metadata.get(TOKEN_BUDGET_MESSAGE_KEY):
                        budget_updates.append({
                            key: message_metadata[key]
                            for key in ("used", "limit", "remaining", "remaining_percent")
                        })
                model_usage = (event.get("output") or {}).get("usage") or {}
                totals = usage.setdefault(event.get("model", "unknown"), {})
                for key, value in model_usage.items():
                    if isinstance(value, (int, float)):
                        totals[key] = totals.get(key, 0) + value
            row = {
                "sample_id": str(sample.id), "epoch": sample.epoch,
                "board": manifest.get("board", "unknown"), "delegate": manifest.get("delegate"),
                "board_read": meta.get("board_read"), "board_route_used": meta.get("board_route_used"),
                "honeypot_evidence": meta.get("honeypot_evidence", []),
                "source": (log.eval.metadata or {}).get("source", manifest.get("source", "unknown")),
                "condition": meta.get("condition", manifest.get("condition", "unknown")),
                "outcome": "error" if sample.error else meta.get("outcome", "incomplete"),
                "success": meta.get("is_success", (score.get("value") or {}).get("main_task_success") == "C" if isinstance(score.get("value"), dict) else score.get("value") == "C"), "delegate_request": meta.get("delegate_request"),
                "model_calls": sum(e.get("event") == "model" for e in events),
                "tool_calls": sum(e.get("event") == "tool" for e in events),
                "forced_submit_calls": sum(e.get("event") == "model" and isinstance(e.get("tool_choice"), dict)
                    and e["tool_choice"].get("name") == "submit" for e in events),
                "model_usage": usage,
                "token_budget_updates": budget_updates,
                "limit": data.get("limit"), "error": data.get("error"),
                "protocol_version": manifest.get("protocol_version", "responsive" if (log.eval.metadata or {}).get("response_options") else "legacy"),
                "response_options": (log.eval.metadata or {}).get("response_options"),
                "help_cases": meta.get("help_cases", (data.get("store") or {}).get("help_cases", {})),
                "direct_requests": meta.get("direct_requests", (data.get("store") or {}).get("direct_requests", [])),
                "blocked_report": meta.get("blocked_report", (data.get("store") or {}).get("blocked_report")),
                "setup_repaired": meta.get("setup_repaired", (data.get("store") or {}).get("setup_repaired", False)),
                "budget_history": meta.get("budget_history", (data.get("store") or {}).get("budget_history", [])),
                "native_log": str(path.relative_to(root)),
            }
            # Inspect discovers legacy JSON logs by timestamp-prefixed filenames.
            # Keep derived exports out of that namespace to avoid phantom runs.
            export = path.parent / f"export-{path.stem}-sample-{sample.epoch}-{str(sample.id).replace('/', '_').replace(':', '_')}"
            export.with_suffix(".json").write_text(json.dumps({"summary": row, "sample": data}, indent=2) + "\n")
            with export.with_suffix(".jsonl").open("w") as f:
                for event in events:
                    f.write(json.dumps(event) + "\n")
            rows.append(row)
    (root / "summary.json").write_text(json.dumps(rows, indent=2) + "\n")
    lines = ["# Run summary", "", "Rows marked `scripted` validate the harness; only rows marked `model` report observed model behavior.", "",
             "| Source | Condition | Outcome | Flag correct | Model calls | Forced submits | Last budget |",
             "|---|---|---|---|---:|---:|---|"]
    for row in rows:
        # Legacy runs carry Mateo's per-call budget message; contract runs carry the counters history.
        if row["token_budget_updates"]:
            last = row["token_budget_updates"][-1]
            budget_text = f"{last['remaining']:,} / {last['limit']:,} left"
        elif row["budget_history"]:
            remaining = row["budget_history"][-1].get("sample_tokens_remaining")
            budget_text = f"{remaining:,} tokens left" if remaining is not None else "not recorded"
        else:
            budget_text = "not recorded"
        lines.append(f"| {row['source']} | {row['condition']} | {row['outcome']} | {row['success']} | {row['model_calls']} | {row['forced_submit_calls']} | {budget_text} |")
    (root / "summary.md").write_text("\n".join(lines) + "\n")
    return rows
