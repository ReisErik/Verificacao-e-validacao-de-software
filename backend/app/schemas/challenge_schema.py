from pydantic import BaseModel
from datetime import datetime

from enum import Enum

class ChallengeType(Enum):
    STREAK = "STREAK"
    TIME = "TIME"

class CreateChallengeSchema(BaseModel):
    name: str
    description: str
    xp_reward: int
    start_date: datetime
    end_date: datetime
    goal: float
    visibility: bool
    type_challenge: ChallengeType

class JoinChallengeSchema(BaseModel):
    challenge_id: int
    invite_id: int
    answer: bool

class UpdateProgressSchema(BaseModel):
    score: float
    challenge_id: int

class ProgressResponseSchema(BaseModel):
    challenge_id: int
    progress: float
    completed: bool



        