"""Count delegate-related references in native model reasoning and tool calls."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from inspect_ai.log import resolve_sample_attachments
from delegate_signals import PATTERNS, find_delegate_signals
from trace_export import native_log_paths, read_native_log


def _reasoning_text(event: dict) -> str:
    """Extract provider-returned reasoning fields after Inspect resolves attachments."""
    chunks: list[str] = []
    output = event.get("output") or {}
    for choice in output.get("choices") or []:
        message = choice.get("message") or {}
        for part in message.get("content") or []:
            if not isinstance(part, dict):
                continue
            if part.get("type") in {"reasoning", "thinking"}:
                value = part.get("reasoning") or part.get("thinking")
                if isinstance(value, str):
                    chunks.append(value)
    return "\n".join(chunks)


def analyze_sample(sample: dict, source: str = "unknown") -> dict:
    events = sample.get("events") or []
    model_events = [event for event in events if event.get("event") == "model"]
    matches = []
    for model_index, event in enumerate(model_events, start=1):
        reasoning = _reasoning_text(event)
        event_matches = find_delegate_signals(reasoning)
        if event_matches:
            matches.append({"model_call": model_index, "model": event.get("model"),
                            "role": event.get("role"), "matches": event_matches})

    delegate_calls = [
        {"event_index": event_index, "arguments": event.get("arguments")}
        for event_index, event in enumerate(events)
        if event.get("event") == "tool" and event.get("function") == "call_delegate"
    ]
    counts = {
        name: sum(
            1 for group in matches for item in group["matches"] if item["pattern"] == name
        )
        for name in PATTERNS
    }
    return {
        "source": source,
        "sample_id": str(sample.get("id", "unknown")),
        "model_calls": len(model_events),
        "reasoning_segments": sum(bool(_reasoning_text(event)) for event in model_events),
        "delegate_related_regex_matches": sum(counts.values()),
        "delegate_related_model_calls": len(matches),
        "pattern_counts": counts,
        "matches": matches,
        "actual_delegate_tool_calls": len(delegate_calls),
        "delegate_tool_calls": delegate_calls,
    }


def analyze_logs(root: Path) -> list[dict]:
    root = Path(root)
    rows = []
    for path in native_log_paths(root):
        log = read_native_log(path)
        for sample in log.samples or []:
            sample = resolve_sample_attachments(sample, "full")
            rows.append(analyze_sample(
                sample.model_dump(mode="json", exclude_none=True),
                source=str(path.relative_to(root)),
            ))
    (root / "delegate-analysis.json").write_text(json.dumps(rows, indent=2) + "\n")
    lines = [
        "# Delegate reasoning analysis", "",
        "Counts are regex matches in provider-returned reasoning fields only; system and user prompts are excluded.", "",
        "Responsive runs also include advisor calls. Model/role labels accompany matches; pooled counts are not worker-only deliberation.", "",
        "| Log | Model calls | Reasoning calls mentioning delegate concepts | Regex matches | Actual call_delegate calls |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['source']}` | {row['model_calls']} | {row['delegate_related_model_calls']} | "
            f"{row['delegate_related_regex_matches']} | {row['actual_delegate_tool_calls']} |"
        )
    for row in rows:
        lines.extend(["", f"## {row['source']}", ""])
        lines.append(f"Pattern counts: `{json.dumps(row['pattern_counts'], sort_keys=True)}`.")
        if not row["matches"]:
            lines.append("No delegate-related regex match was found in returned reasoning.")
        else:
            for group in row["matches"]:
                for match in group["matches"]:
                    lines.append(f"- model call {group['model_call']} ({group.get('model')}, role={group.get('role')}), `{match['pattern']}`: {match['snippet']}")
        lines.append(f"Actual `call_delegate` tool calls: {row['actual_delegate_tool_calls']}.")
    (root / "delegate-analysis.md").write_text("\n".join(lines) + "\n")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Run or results directory containing native .eval logs")
    args = parser.parse_args()
    print(json.dumps(analyze_logs(args.root), indent=2))


if __name__ == "__main__":
    main()
