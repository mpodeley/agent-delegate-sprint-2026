"""Run a deterministic local mock cohort; never call an external model."""
import json
from pathlib import Path

from inspect_ai import eval
from inspect_ai.model import ChatCompletionChoice, ChatMessageAssistant, ModelOutput, get_model
from inspect_ai.tool import ToolCall

from channel_lab.cli import init
from channel_lab.paired_eval import cohort

ROOT = Path(__file__).resolve().parent.parent
seen = set()


def mock_output(messages, tools, tool_choice, config):
    task_text = next(m.text for m in messages if m.role == "user")
    actor = "worker-a" if "You are worker-a." in task_text else "worker-b"
    assert ("You are worker-a." in task_text) != ("You are worker-b." in task_text)
    assert messages[0].role == "system" and "Do not communicate" in messages[0].text
    seen.add(actor)
    if any(m.role == "tool" for m in messages):
        function, arguments = "submit", {"answer":"SCRIPTED MOCK: workspace checked; task intentionally unsolved."}
    else:
        function = next(t.name for t in tools if t.name != "submit")
        arguments = {"command":"pwd && cat TASK.md"}
    return ModelOutput(model="mockllm/model", choices=[ChatCompletionChoice(
        message=ChatMessageAssistant(content="", tool_calls=[
            ToolCall(id=actor + "-" + function, function=function, arguments=arguments)
        ]), stop_reason="tool_calls",
    )])


if __name__ == "__main__":
    init()
    logs = eval(cohort(worker_message_limit=12),
                model=get_model("mockllm/model",custom_outputs=mock_output),
                log_dir=str(ROOT / "runtime/mock-integration"), display="plain")
    assert len(logs) == 1 and logs[0].status == "success"
    sample = logs[0].samples[0]
    assert sample.error is None and seen == {"worker-a", "worker-b"}
    for actor in ("worker_a", "worker_b"):
        assert len(sample.metadata[actor + "_messages"]) >= 5
        assert sample.metadata[actor + "_limit"] is None
    scores = sample.scores["cohort_outcomes"]
    assert scores.value == {"worker_a_task":0, "worker_b_task":0}
    assert scores.metadata["journal"]["events"] == []
    assert len([o for o in scores.metadata["journal"]["objects"] if o["key"].startswith("build-notes/")]) == 3
    print(json.dumps({"kind":"local_mock_integration","passed":True,
                      "workers":sorted(seen),"real_model_calls":0,"log":logs[0].location},indent=2))
