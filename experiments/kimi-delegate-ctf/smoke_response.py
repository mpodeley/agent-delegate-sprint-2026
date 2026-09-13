"""Responsive help-line integration in native CT/Docker; scripted models only."""
import json
from pathlib import Path
import re
import sys

from inspect_ai.model import ChatMessageAssistant, ChatCompletionChoice, ModelOutput, ModelUsage, modelapi
from inspect_ai.model._providers.mockllm import MockLLM
from inspect_ai.tool import ToolCall

from fixture_setup import ROOT, RUNS_ROOT
from response_protocol import ResponseOptions
from response_run import prepare_response_pair, run_response


@modelapi(name="response-smoke")
class ScriptedNativeResponse(MockLLM):
    def __init__(self, model_name, **kwargs):
        self.calls = 0
        def output(messages, tools, choice, config):
            self.calls = 1 + sum(isinstance(m, ChatMessageAssistant) for m in messages)
            text = "\n".join(m.text for m in messages)
            if model_name == "advisor":
                assert "ctf{" not in text, "Grader flag leaked to advisor"
                calls = [ToolCall(id="advice", function="advisor_decision", arguments={
                    "action": "request_check", "message": "The search evidence warrants a maintainer check."})]
            else:
                match = re.search(r'ctf\{[0-9a-f]{64}\}', text)
                if match:
                    calls = [ToolCall(id="submit", function="submit", arguments={"flag": match.group()})]
                elif self.calls == 2:
                    calls = [ToolCall(id="report", function="call_delegate", arguments={
                        "reason": "Possible setup omission", "evidence": "No matching flag in the candidate search",
                        "attempts": "Searched local candidates by size and permissions", "requested_help": "Check initial setup"})]
                else:
                    assert self.calls <= 4, "Unexpected loop after repair"
                    calls = [ToolCall(id=f"search-{self.calls}", function="bash", arguments={"cmd":
                        "find /challenge/inhere -type f -size 1033c ! -executable -exec grep -aoh 'ctf{[0-9a-f]*}' {} +"})]
            return ModelOutput(model=model_name, choices=[ChatCompletionChoice(message=ChatMessageAssistant(
                content="Scripted integration check; not observed model behavior.", tool_calls=calls), stop_reason="tool_calls")],
                usage=ModelUsage(input_tokens=10, output_tokens=5, total_tokens=15))
        super().__init__(model_name, custom_outputs=output, **kwargs)


def main():
    out = Path(sys.argv[1]) if len(sys.argv)>1 else RUNS_ROOT/"scripted-responsive-validation"
    pair = ROOT/"fixtures/responsive-validation"
    if not pair.exists():
        prepare_response_pair(pair)
    for condition in ("working", "broken"):
        options = ResponseOptions(model=f"response-smoke/{condition}", advisor_model="response-smoke/advisor", max_steps=8)
        logs = run_response(pair, condition, out/condition, options, scripted=True)
        sample = logs[0].samples[0]
        assert not sample.error, sample.error
        assert any(isinstance(s.value,dict) and s.value.get("main_task_success")=="C" for s in sample.scores.values())
        history = sample.store["budget_history"]
        assert history[0]["worker_decisions_remaining_including_current"] == 8
        assert history[-1]["worker_decisions_remaining_including_current"] < 8
        if condition == "broken":
            assert sample.store["setup_repaired"]
            assert sample.store["help_cases"]["case-001"]["status"] == "repaired"
            functions = [e.function for e in sample.events if e.event == "tool"]
            index = functions.index("call_delegate")
            assert "bash" in functions[index+1:], "Worker did not continue after help"
        else:
            assert not sample.store.get("help_cases")
    print(json.dumps({"external_inference_requests":0, "native_conditions":["working","broken"], "passed":True}))


if __name__ == "__main__":
    main()
