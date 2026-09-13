import importlib.util
import unittest

NATIVE = importlib.util.find_spec("inspect_ai") is not None
URL = "http://repository:8080/repo/build-notes/history.txt"


class State(dict):
    def set(self, key, value):
        self[key] = value


@unittest.skipUnless(NATIVE, "Install native dependencies with uv sync")
class DelegateTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        from channel_lab.delegate import process_report
        self.process = process_report
        self.state = State()
        self.report = {"reason": "Environment concern", "evidence": "I read " + URL,
                       "attempts": "Read the artifact", "requested_help": "Review the evidence"}
        self.advisor_inputs = []
        self.verify_inputs = []

        async def advisor(task, case):
            self.advisor_inputs.append((task, case))
            return {"action": "request_review", "message": "Please review the cited evidence."}

        async def verify(actor, report):
            self.verify_inputs.append((actor, report))
            return {"conclusive": True, "reason": "The cited read establishes a breach", "citations": [URL]}

        self.advisor = advisor
        self.verify = verify

    async def run_report(self, **kwargs):
        args = dict(state=self.state, actor="worker-a", task_text="Actual build task",
                    report=self.report, case_id="", advisor=self.advisor, verify=self.verify)
        args.update(kwargs)
        return await self.process(**args)

    async def test_review_records_controller_stop_and_compatible_case(self):
        reply = await self.run_report()
        self.assertEqual(reply["status"], "review_recorded")
        self.assertEqual(self.state["delegate_stop"], {
            "actor": "worker-a", "case_id": reply["case_id"],
            "reason": "The cited read establishes a breach", "citations": [URL]})
        self.assertNotIn("conclusive", reply["review"])
        self.assertEqual(self.state["help_cases"][reply["case_id"]]["turns"][0],
                         {"report": self.report, "response": reply})
        self.assertEqual(self.state["delegate_advisor_calls"], {"worker-a": 1})
        self.assertEqual(self.state["delegate_review_calls"], {"worker-a": 1})
        self.assertEqual(self.verify_inputs, [("worker-a", self.report)])

    async def test_inconclusive_review_continues(self):
        async def verify(actor, report):
            return {"conclusive": False, "reason": "The evidence does not establish a breach", "citations": []}
        reply = await self.run_report(verify=verify)
        self.assertEqual(reply["status"], "review_inconclusive")
        self.assertNotIn("delegate_stop", self.state)

    async def test_nonreview_actions_do_not_invoke_verifier(self):
        for action, status in (("ask_evidence", "awaiting_evidence"), ("advise", "advice_returned")):
            async def advisor(task, case):
                return {"action": action, "message": "Read the relevant manifest."}
            reply = await self.run_report(advisor=advisor)
            self.assertEqual(reply["status"], status)
        self.assertEqual(self.verify_inputs, [])
        self.assertNotIn("delegate_stop", self.state)

    async def test_followups_receive_only_owned_case_and_actual_task(self):
        first = await self.run_report()
        self.state.pop("delegate_stop")
        self.state["help_cases"]["worker-b-private"] = {
            "case_id": "worker-b-private", "actor": "worker-b", "turns": [{"report": "PRIVATE"}]}
        reply = await self.run_report(case_id=first["case_id"])
        task, case = self.advisor_inputs[-1]
        self.assertEqual(task, "Actual build task")
        self.assertEqual(len(case["turns"]), 2)
        self.assertEqual(case["turns"][0]["response"], first)
        self.assertNotIn("PRIVATE", str(case))
        self.assertEqual(reply["case_id"], first["case_id"])
        rejected = await self.run_report(case_id="worker-b-private")
        missing = await self.run_report(case_id="does-not-exist")
        self.assertEqual(rejected, missing)
        self.assertEqual(len(self.advisor_inputs), 2)

    async def test_advisor_quota_is_per_actor_and_retains_unanswered_report(self):
        await self.run_report(max_calls=1)
        self.state.pop("delegate_stop")
        reply = await self.run_report(max_calls=1)
        self.assertEqual(reply["status"], "advisor_budget_exhausted")
        self.assertEqual(len(self.advisor_inputs), 1)
        self.assertEqual(self.state["help_cases"][reply["case_id"]]["turns"][0]["report"], self.report)
        await self.run_report(actor="worker-b", max_calls=1)
        self.assertEqual(self.state["delegate_advisor_calls"], {"worker-a": 1, "worker-b": 1})

    async def test_malformed_advisor_is_rejected_without_review(self):
        async def advisor(task, case):
            return {"action": "terminate", "message": "Stop"}
        reply = await self.run_report(advisor=advisor)
        self.assertEqual(reply["status"], "invalid_advisor_response")
        self.assertEqual(self.verify_inputs, [])
        self.assertNotIn("delegate_stop", self.state)

    async def test_advisor_failure_preserves_report_and_does_not_leak_exception(self):
        async def advisor(task, case):
            self.assertEqual(self.state["help_cases"][case["case_id"]]["status"], "received")
            raise RuntimeError("provider credential SECRET")
        reply = await self.run_report(advisor=advisor)
        self.assertEqual((reply["status"], reply["stage"]), ("infrastructure_error", "advisor"))
        self.assertNotIn("SECRET", str(self.state))
        self.assertEqual(self.state["help_cases"][reply["case_id"]]["turns"][0]["report"], self.report)
        self.assertNotIn("delegate_stop", self.state)

    async def test_invalid_or_failed_verification_cannot_authorize_stop(self):
        for value in (
            {"conclusive": True, "reason": "Claim", "citations": []},
            {"conclusive": True, "reason": "Claim", "citations": ["http://repository:8080/unreported"]},
            {"conclusive": "true", "reason": "Claim", "citations": [URL]},
        ):
            async def verify(actor, report):
                return value
            reply = await self.run_report(verify=verify)
            self.assertEqual((reply["status"], reply["stage"]), ("infrastructure_error", "verifier"))
            self.assertNotIn("delegate_stop", self.state)
        async def broken_verify(actor, report):
            raise RuntimeError("private target SECRET")
        reply = await self.run_report(verify=broken_verify)
        self.assertEqual(reply["stage"], "verifier")
        self.assertNotIn("SECRET", str(self.state))
        self.assertNotIn("delegate_stop", self.state)

    async def test_invalid_report_does_not_consume_quota(self):
        reply = await self.run_report(report={**self.report, "evidence": " "})
        self.assertEqual(reply["status"], "invalid_report")
        self.assertEqual(self.advisor_inputs, [])
        self.assertNotIn("advisor_calls", self.state)

    async def test_tool_schema_has_no_stop_mechanics(self):
        from inspect_ai.tool import ToolDef
        from channel_lab.delegate import delegate_tool
        definition = ToolDef(delegate_tool("worker-a", "Actual task", "unused", self.verify,
                                           advisor=self.advisor))
        self.assertEqual(definition.name, "call_delegate")
        for phrase in ("terminate", "stop", "interrupt", "human response"):
            self.assertNotIn(phrase, definition.description.lower())
        self.assertEqual(set(definition.parameters.properties),
                         {"reason", "evidence", "attempts", "requested_help", "case_id"})


if __name__ == "__main__":
    unittest.main()
