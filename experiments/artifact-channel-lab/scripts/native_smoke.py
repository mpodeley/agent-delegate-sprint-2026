"""Scripted native CT cohort, including isolated tools and native submission."""
from pathlib import Path
import sys

from inspect_ai.model import ChatCompletionChoice, ChatMessageAssistant, ModelOutput, ModelUsage, modelapi
from inspect_ai.model._providers.mockllm import MockLLM
from inspect_ai.tool import ToolCall

from channel_lab.native_run import run_native


@modelapi(name="artifact-smoke")
class ScriptedCohort(MockLLM):
    def __init__(self, model_name, **kwargs):
        def output(messages, tools, choice, config):
            prompt = next(m.text for m in messages if m.role == "user")
            actor = "worker_a" if "You are worker-a." in prompt else "worker_b"
            names = {t.name for t in tools}
            assert names == {actor + "_bash", "submit"}, names
            assert "Do not communicate" in messages[0].text
            if any(m.role == "tool" for m in messages):
                command = ToolCall(id=actor + "-submit", function="submit", arguments={})
            else:
                command = ToolCall(id=actor + "-shell", function=actor + "_bash", arguments={"cmd":
                    "pwd && cat TASK.md && curl -fsS http://repository:8080/repo/packages/cache-manifest.json"})
            return ModelOutput(model=model_name, choices=[ChatCompletionChoice(
                message=ChatMessageAssistant(content="Scripted infrastructure test.",tool_calls=[command]),
                stop_reason="tool_calls")], usage=ModelUsage(input_tokens=10, output_tokens=5,total_tokens=15))
        super().__init__(model_name, custom_outputs=output, **kwargs)


if __name__ == "__main__":
    logs = run_native(Path(sys.argv[1]), "artifact-smoke/model", max_steps=3, scripted=True)
    sample = logs[0].samples[0]
    for actor in ("worker_a", "worker_b"):
        history = sample.metadata[actor + "_messages"]
        assert any(t["function"] == "submit" for m in history for t in m.get("tool_calls") or [])
        assert any(actor + "_bash" == t["function"] for m in history for t in m.get("tool_calls") or [])
    names = {t.function for m in sample.messages for t in getattr(m, "tool_calls", None) or []}
    assert {"worker_a_bash", "worker_b_bash", "submit"} <= names
    print("Native paired histories, worker routing, journal and CTF export: passed")
