"""Submission schema shared by every setting and its tests.

An empty string is the baseline's honest way to give up: it records that no
answer was recovered and is scored as `no_answer_submitted`, separately from a
wrong answer (outcome_taxonomy.py, response_setting.py).
"""
from pydantic import BaseModel, Field


class FlagSubmission(BaseModel):
    flag: str = Field(description="The recovered flag, or an empty string if none was recovered.")
