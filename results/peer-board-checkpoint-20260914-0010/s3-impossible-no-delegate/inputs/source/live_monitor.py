"""Local live monitor for provider-returned reasoning from a Kimi CTF run.

The runner appends a JSONL sidecar after every completed policy-loop response. This module turns
that sidecar into a small local dashboard. It never calls a model or sends text
off-machine. Its vectors are deterministic hashed token features, useful for
grouping repeated lines of investigation but not a semantic-model judgement.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import math
import os
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlparse

from delegate_signals import PATTERNS, find_delegate_signals


MONITOR_PATH_ENV = "KIMI_CTF_MONITOR_PATH"
DIMENSIONS = 256
CLUSTER_THRESHOLD = 0.24
TOKEN_RE = re.compile(r"[a-z][a-z0-9_-]{2,}", re.IGNORECASE)
STOPWORDS = frozenset({
    "the", "and", "that", "this", "with", "from", "for", "have", "has", "not", "are", "was",
    "will", "can", "could", "should", "need", "into", "then", "than", "there", "their", "about",
    "using", "use", "after", "before", "through", "only", "also", "but", "just", "may", "might",
})


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit(path: str | Path | None, record: dict[str, Any]) -> None:
    """Append a flush-safe local event. Monitoring must never affect an eval."""
    if not path:
        return
    try:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        event = {"recorded_at": utc_now(), **record}
        with destination.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event, ensure_ascii=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
    except OSError:
        # The native eval is more important than a dashboard disk-write failure.
        return


def record_run_started(path: str | Path | None, **metadata: Any) -> None:
    emit(path, {"event": "run_started", **metadata})


def _json_message(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json", exclude_none=True)
    return value if isinstance(value, dict) else {}


def _content_parts(message: dict[str, Any]) -> list[dict[str, Any]]:
    content = message.get("content") or []
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return [part for part in content if isinstance(part, dict)]


def reasoning_from_message(message: dict[str, Any]) -> str:
    return "\n".join(
        str(part.get("reasoning") or part.get("thinking") or "")
        for part in _content_parts(message)
        if part.get("type") in {"reasoning", "thinking"}
    ).strip()


def text_from_message(message: dict[str, Any]) -> str:
    return "\n".join(
        str(part.get("text") or "") for part in _content_parts(message)
        if part.get("type") == "text"
    ).strip()


def trailing_tool_results(messages: list[Any]) -> list[dict[str, str]]:
    results = []
    for message in reversed(messages):
        item = _json_message(message)
        if item.get("role") != "tool":
            break
        results.append({
            "function": str(item.get("function") or "tool"),
            "content": str(item.get("content") or "")[:2_000],
        })
    return list(reversed(results))


def record_model_turn(
    path: str | Path | None,
    sequence: int,
    model_output: Any,
    input_messages: list[Any],
    budget: dict[str, int | float] | None = None,
) -> None:
    """Record one response returned to the policy loop immediately after generation."""
    output = _json_message(model_output)
    choices = output.get("choices") or []
    message = (choices[0].get("message") or {}) if choices else {}
    tool_calls = message.get("tool_calls") or []
    emit(path, {
        "event": "model_turn",
        "sequence": sequence,
        "model": output.get("model"),
        "reasoning": reasoning_from_message(message),
        "text": text_from_message(message),
        "proposed_tools": [
            {"function": call.get("function"), "arguments": call.get("arguments")}
            for call in tool_calls if isinstance(call, dict)
        ],
        "prior_tool_results": trailing_tool_results(input_messages),
        "usage": output.get("usage") or {},
        "budget": budget or {},
    })


def record_delegate_executed(path: str | Path | None, request: dict[str, Any]) -> None:
    emit(path, {"event": "delegate_executed", "request": request})


def record_environment_case_opened(path: str | Path | None, case: dict[str, Any]) -> None:
    emit(path, {"event": "environment_case_opened", "case": case})


def record_run_finished(path: str | Path | None, status: str, **metadata: Any) -> None:
    emit(path, {"event": "run_finished", "status": status, **metadata})


def read_records(path: str | Path) -> list[dict[str, Any]]:
    source = Path(path)
    if not source.exists():
        return []
    records = []
    for line in source.read_text(encoding="utf-8").splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue  # A concurrent append may expose an incomplete last line.
        if isinstance(item, dict):
            records.append(item)
    return records


def token_features(text: str) -> list[str]:
    terms = [word.lower() for word in TOKEN_RE.findall(text) if word.lower() not in STOPWORDS]
    return terms + [f"{left}:{right}" for left, right in zip(terms, terms[1:])]


def local_embedding(text: str, dimensions: int = DIMENSIONS) -> list[float]:
    vector = [0.0] * dimensions
    for feature in token_features(text):
        digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
        value = int.from_bytes(digest, "big")
        vector[value % dimensions] += 1.0 if value & 1 else -1.0
    norm = math.sqrt(sum(value * value for value in vector))
    return [value / norm for value in vector] if norm else vector


def cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def cluster_episodes(episodes: list[dict[str, Any]], threshold: float = CLUSTER_THRESHOLD) -> list[dict[str, Any]]:
    clusters: list[dict[str, Any]] = []
    for episode in episodes:
        vector = local_embedding(episode.get("reasoning") or episode.get("text") or "")
        if not any(vector):
            episode["cluster"] = None
            continue
        similarities = [cosine(vector, cluster["centroid"]) for cluster in clusters]
        index = max(range(len(similarities)), key=similarities.__getitem__) if similarities else None
        if index is None or similarities[index] < threshold:
            clusters.append({"centroid": vector, "members": [episode]})
            episode["cluster"] = len(clusters)
            continue
        cluster = clusters[index]
        count = len(cluster["members"])
        centroid = [(value * count + incoming) / (count + 1)
                    for value, incoming in zip(cluster["centroid"], vector)]
        norm = math.sqrt(sum(value * value for value in centroid)) or 1.0
        cluster["centroid"] = [value / norm for value in centroid]
        cluster["members"].append(episode)
        episode["cluster"] = index + 1

    summaries = []
    for index, cluster in enumerate(clusters, start=1):
        words = Counter()
        signal_turns = 0
        for episode in cluster["members"]:
            words.update(token_features(episode.get("reasoning") or episode.get("text") or ""))
            signal_turns += int(bool(episode["signals"]))
        label_terms = [word for word, _ in words.most_common(8) if ":" not in word][:4]
        summaries.append({
            "id": index,
            "label": " · ".join(label_terms) or "unlabeled reasoning",
            "turns": len(cluster["members"]),
            "last_sequence": cluster["members"][-1]["sequence"],
            "delegate_signal_turns": signal_turns,
        })
    return summaries


def snapshot(path: str | Path) -> dict[str, Any]:
    records = read_records(path)
    episodes = []
    delegate_requests = []
    environment_cases = []
    run_metadata = {}
    finished = None
    for record in records:
        if record.get("event") == "run_started":
            run_metadata = {key: value for key, value in record.items()
                            if key not in {"event", "recorded_at"}}
        elif record.get("event") == "model_turn":
            reasoning = str(record.get("reasoning") or "")
            episodes.append({
                "sequence": record.get("sequence"),
                "recorded_at": record.get("recorded_at"),
                "reasoning": reasoning,
                "text": str(record.get("text") or ""),
                "signals": find_delegate_signals(reasoning),
                "proposed_tools": record.get("proposed_tools") or [],
                "prior_tool_results": record.get("prior_tool_results") or [],
                "budget": record.get("budget") or {},
            })
        elif record.get("event") == "delegate_executed":
            delegate_requests.append(record)
        elif record.get("event") == "environment_case_opened":
            environment_cases.append(record)
        elif record.get("event") == "run_finished":
            finished = record
    clusters = cluster_episodes(episodes)
    counts = Counter(match["pattern"] for episode in episodes for match in episode["signals"])
    return {
        "generated_at": utc_now(),
        "stream_path": str(Path(path).resolve()),
        "run": run_metadata,
        "state": (f"finished_{finished.get('status', 'unknown')}" if finished else
                  "paused_environment_case" if environment_cases else "paused_delegate"
                  if delegate_requests else "streaming" if episodes else "waiting"),
        "turn_count": len(episodes),
        "reasoning_turn_count": sum(bool(episode["reasoning"]) for episode in episodes),
        "delegate_signal_count": sum(counts.values()),
        "delegate_signal_turns": sum(bool(episode["signals"]) for episode in episodes),
        "delegate_requests": delegate_requests,
        "environment_cases": environment_cases,
        "finished": finished,
        "pattern_counts": dict(counts),
        "patterns": {name: definition["label"] for name, definition in PATTERNS.items()},
        "latest_budget": episodes[-1]["budget"] if episodes else {},
        "clusters": clusters,
        "episodes": episodes,
    }


PAGE = r'''<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kimi live monitor</title>
<style>
  :root { color-scheme: dark; --bg:#101216; --panel:#171b22; --line:#2b3240; --text:#f2f4f8; --muted:#9ca6b8; --mint:#6ee7b7; --amber:#fbbf24; --red:#fb7185; }
  * { box-sizing:border-box } body { margin:0; background:var(--bg); color:var(--text); font:14px/1.45 ui-sans-serif,system-ui,sans-serif; }
  main { max-width:1280px; margin:0 auto; padding:28px 20px 56px; } h1,h2,p { margin:0 } h1 { font-size:24px; letter-spacing:-.03em } h2 { font-size:14px; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; }
  .top { display:flex; justify-content:space-between; gap:20px; align-items:start; margin-bottom:22px }.sub { color:var(--muted); margin-top:5px; max-width:720px }.badge { border:1px solid var(--line); border-radius:999px; padding:5px 10px; color:var(--mint); font-variant-numeric:tabular-nums; white-space:nowrap }
  .metrics { display:grid; grid-template-columns:repeat(6,minmax(120px,1fr)); gap:10px; margin-bottom:16px }.card,.episode { background:var(--panel); border:1px solid var(--line); border-radius:10px }.metric { padding:14px }.metric b { display:block; font-size:24px; font-variant-numeric:tabular-nums }.metric span { color:var(--muted); font-size:12px }
  .grid { display:grid; grid-template-columns:1.15fr .85fr; gap:16px }.panel { padding:16px }.panel + .panel { margin-top:16px }.clusters { display:grid; gap:8px; margin-top:12px }.cluster { padding:10px; border-left:3px solid #64748b; background:#121720; border-radius:0 7px 7px 0 }.cluster small { color:var(--muted) }
  .episode { padding:14px; margin-top:10px }.episode-head { display:flex; gap:8px; justify-content:space-between; color:var(--muted); font-variant-numeric:tabular-nums }.tags { display:flex; gap:5px; flex-wrap:wrap; margin-top:8px }.tag { font-size:12px; padding:2px 7px; border-radius:999px; background:#273449; color:#c9dcff }.tag.signal { background:#47321a; color:var(--amber) }.tag.actual { background:#4a1824; color:#fecdd3 } pre { white-space:pre-wrap; overflow-wrap:anywhere; font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace; color:#d9e1ef; margin:10px 0 0 }.empty { color:var(--muted); padding:14px 0 }.note { color:var(--muted); font-size:12px; margin-top:12px } @media(max-width:800px){.metrics{grid-template-columns:repeat(2,1fr)}.grid{grid-template-columns:1fr}.top{display:block}.badge{display:inline-block;margin-top:12px}}
</style>
<main>
  <div class="top"><div><h1>Returned-reasoning monitor</h1><p class="sub">Local stream for the Kimi CTF. Regex signals scan only reasoning returned by the provider; they do not reveal hidden chain-of-thought or prove intent.</p></div><span id="state" class="badge">connecting</span></div>
  <section id="metrics" class="metrics"></section>
  <div class="grid"><section class="card panel"><h2>Turn timeline</h2><div id="timeline"></div></section><aside><section class="card panel"><h2>Investigation clusters</h2><div id="clusters"></div><p class="note">Clusters use local deterministic hashed token vectors. They group recurring lines of investigation; they are not semantic-model labels.</p></section><section class="card panel"><h2>Regex signals</h2><div id="signals"></div><p class="note">Edit <code>delegate_patterns.json</code> before a run to change the signal groups.</p></section></aside></div>
</main>
<script>
const el = id => document.getElementById(id); const node = (tag, text, cls) => { const x=document.createElement(tag); if(text!==undefined)x.textContent=text; if(cls)x.className=cls; return x; };
function metric(value,label){const box=node('div',undefined,'card metric');box.append(node('b',String(value)),node('span',label));return box}
function render(data){
  el('state').textContent=data.state.replace('_',' ')+' · '+data.turn_count+' turns';
  const budget=data.latest_budget||{}; const m=el('metrics');m.replaceChildren(metric(data.turn_count,'model turns'),metric(data.delegate_signal_count,'delegate regex matches'),metric(data.delegate_signal_turns,'turns with a signal'),metric(data.environment_cases.length,'actual cases opened'),metric(data.delegate_requests.length,'actual delegate calls'),metric(budget.remaining===undefined?'—':Number(budget.remaining).toLocaleString(),'tokens remaining'));
  const signals=el('signals');signals.replaceChildren();Object.entries(data.patterns||{}).forEach(([key,label])=>{const p=node('p');p.append(node('b',(data.pattern_counts[key]||0)+' '),document.createTextNode(label));signals.append(p)});if(!Object.keys(data.patterns||{}).length)signals.append(node('p','No patterns loaded.','empty'));
  const clusters=el('clusters');clusters.replaceChildren();(data.clusters||[]).slice().reverse().forEach(c=>{const x=node('div',undefined,'cluster');x.append(node('div','cluster '+c.id+' · '+c.label),node('small',c.turns+' turns · last '+c.last_sequence+' · '+c.delegate_signal_turns+' signal turns'));clusters.append(x)});if(!(data.clusters||[]).length)clusters.append(node('p','Waiting for a returned reasoning turn.','empty'));
  const timeline=el('timeline');timeline.replaceChildren();(data.episodes||[]).slice().reverse().forEach(ep=>{const x=node('article',undefined,'episode');const h=node('div',undefined,'episode-head');h.append(node('span','turn '+ep.sequence+(ep.cluster?' · cluster '+ep.cluster:'')),node('span',new Date(ep.recorded_at).toLocaleTimeString()));x.append(h);const tags=node('div',undefined,'tags');ep.signals.forEach(s=>tags.append(node('span',s.label+': '+s.match,'tag signal')));(ep.proposed_tools||[]).forEach(t=>tags.append(node('span','proposed '+t.function,'tag')));if(!ep.reasoning)tags.append(node('span','no returned reasoning','tag'));x.append(tags);if((ep.proposed_tools||[]).length)x.append(node('pre','next tools\\n'+ep.proposed_tools.map(t=>t.function+' '+JSON.stringify(t.arguments||{})).join('\\n')));if((ep.prior_tool_results||[]).length)x.append(node('pre','previous tool results\\n'+ep.prior_tool_results.map(t=>t.function+': '+t.content).join('\\n')));if(ep.reasoning)x.append(node('pre',ep.reasoning)); else if(ep.text)x.append(node('pre',ep.text));timeline.append(x)});if(!(data.episodes||[]).length)timeline.append(node('p','The dashboard will update after the first completed Kimi response.','empty'));
}
async function poll(){try{render(await (await fetch('/api/snapshot',{cache:'no-store'})).json())}catch(e){el('state').textContent='monitor unavailable'}}poll();setInterval(poll,2000);
</script>'''


def make_handler(stream_path: Path):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            route = urlparse(self.path).path
            if route == "/api/snapshot":
                body = json.dumps(snapshot(stream_path), ensure_ascii=False).encode("utf-8")
                content_type = "application/json; charset=utf-8"
            elif route == "/":
                body = PAGE.encode("utf-8")
                content_type = "text/html; charset=utf-8"
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: Any) -> None:
            return
    return Handler


def serve(stream_path: Path, port: int) -> None:
    server = ThreadingHTTPServer(("127.0.0.1", port), make_handler(stream_path))
    print(f"Kimi live monitor: http://127.0.0.1:{port}  (watching {stream_path})", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["serve", "snapshot"])
    parser.add_argument("stream", type=Path, help="live-monitor.jsonl path; it may not exist yet")
    parser.add_argument("--port", type=int, default=8099)
    args = parser.parse_args()
    if args.command == "serve":
        serve(args.stream, args.port)
    else:
        print(json.dumps(snapshot(args.stream), indent=2))


if __name__ == "__main__":
    main()
