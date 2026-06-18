from sqlmodel import SQLModel, Field
from datetime import datetime, UTC

class ChallengeLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    challenge_id : int = Field(foreign_key="challenge.id")
    user_id: int = Field(foreign_key="user.id")
    score: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))