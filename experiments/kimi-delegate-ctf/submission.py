"""Submission schema shared by the responsive task and its tests."""
from pydantic import BaseModel, Field


class FlagSubmission(BaseModel):
    flag: str = Field(description="The recovered flag; submit only after verification.")
