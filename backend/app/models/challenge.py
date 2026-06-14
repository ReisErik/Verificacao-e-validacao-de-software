from sqlmodel import SQLModel, Field
from datetime import datetime
from app.schemas.challenge_schema import ChallengeType

class Challenge(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    owner: int | None = Field(default=None, foreign_key="user.id")
    name: str
    description: str
    xp_reward: int
    start_date: datetime
    end_date: datetime
    goal: int
    visibility: bool = False
    type_challenge: ChallengeType
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
