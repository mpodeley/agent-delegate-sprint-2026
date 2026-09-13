"""Options for the delegate study, mapped onto the shared worker contract.

The agent-facing text lives in worker_policy.py, shared by both arms (baseline,
delegate). This module keeps the study's option set, the mapping to
WorkerOptions, and thin wrappers so older call sites keep working.
"""
import os
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from worker_policy import (
    HELP_TOOL_NAMES, WorkerOptions, budget_message,
    budget_snapshot as _budget_snapshot, worker_contract as _worker_contract,
)

__all__ = ["ResponseOptions", "options_from_env", "worker_contract", "budget_snapshot",
           "budget_message", "HELP_TOOL_NAMES"]


class ResponseOptions(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    # "none" is the baseline: task tools only, no help route in the contract.
    intermediary: Literal["none", "delegate"] = "delegate"
    budget_feedback: bool = True
    scope_line: Literal["strict", "plain", "none"] = "strict"
    setup_caveat: bool = False
    model: str
    advisor_model: str
    max_steps: int = Field(default=40, ge=2)
    token_limit: int = Field(default=60000, ge=1000)
    time_limit: int = Field(default=1200, ge=1)
    max_output_tokens: int = Field(default=4096, ge=128)
    advisor_output_tokens: int = Field(default=1024, ge=128)
    max_advisor_calls: int = Field(default=4, ge=1)

    @property
    def worker(self) -> WorkerOptions:
        """The contract options this study passes to the shared plain-worker policy."""
        return WorkerOptions(
            help_arm=self.intermediary, help_mechanism="responsive", scope_line=self.scope_line,
            budget_feedback=self.budget_feedback, setup_caveat=self.setup_caveat,
            max_steps=self.max_steps, token_limit=self.token_limit, time_limit=self.time_limit,
            max_advisor_calls=self.max_advisor_calls,
        )

    @property
    def help_tool_name(self) -> str | None:
        return self.worker.tool_name


def options_from_env():
    return ResponseOptions.model_validate_json(os.environ["CTF_RESPONSE_OPTIONS"])


def worker_contract(options: ResponseOptions, environment_description: str = "") -> str:
    return _worker_contract(options.worker, environment_description)


def budget_snapshot(options: ResponseOptions, decision, limits, advisor_calls=0):
    return _budget_snapshot(options.worker, decision, limits, advisor_calls)
