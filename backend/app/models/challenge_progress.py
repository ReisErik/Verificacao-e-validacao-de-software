from sqlmodel import SQLModel, Field

class ChallengeProgress(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    challenge_id: int = Field(foreign_key="challenge.id")
    user_id: int = Field(foreign_key="user.id")
    current_progress: float = 0
    completed: bool = False