from sqlmodel import SQLModel, Field
from datetime import datetime

class ChallengeGroup(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    winner_id: int = Field(default=None, foreign_key="user.id")
    challenge_id: int = Field(default=None, foreign_key="challenge.id")
    participant: int = Field(default=None, foreign_key="user.id")
    visibility: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
