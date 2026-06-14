from sqlmodel import SQLModel, Field
from datetime import datetime, UTC

class ChallengeParticipant(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    challenge_id: int | None = Field(default=None, foreign_key="challenge.id", ondelete="CASCADE")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))