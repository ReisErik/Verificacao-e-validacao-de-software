from sqlmodel import SQLModel, Field
from datetime import date

class ChallengeProgress(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    challenge_id: int = Field(foreign_key="challenge.id", ondelete="CASCADE")
    user_id: int = Field(foreign_key="user.id")
    current_progress: float = 0
    xp_granted: bool = False
    completed: bool = False
    last_update: date | None = None