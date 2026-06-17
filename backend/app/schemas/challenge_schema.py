from pydantic import BaseModel
from datetime import datetime

from enum import Enum

class ChallengeType(Enum):
    STREAK = "STREAK"
    TIME = "TIME"

class CreateChallengeSchema(BaseModel):
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    goal: float
    visibility: bool
    type_challenge: ChallengeType
    category: str

class ChallengeResponseSchema(BaseModel):
    id: int
    owner: int
    name: str
    description: str
    xp_reward: int
    start_date: datetime
    end_date: datetime
    goal: float
    visibility: bool
    type_challenge: ChallengeType
    category: str

class JoinChallengeSchema(BaseModel):
    challenge_id: int
    invite_id: int
    answer: bool

class UpdateProgressSchema(BaseModel):
    challenge_id: int
    score: float

class ProgressResponseSchema(BaseModel):
    challenge_id: int
    current_progress: float
    completed: bool



        