from sqlmodel import SQLModel, Field

class ChallengeStreak(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_challenge : int = Field(default=None, foreign_key="challenge.id")
    goal_days: int