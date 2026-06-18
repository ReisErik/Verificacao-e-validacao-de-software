from sqlmodel import SQLModel, Field
from datetime import date

class ChallengeInvite(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sender_id: int | None = Field(default=None, foreign_key="user.id")
    sender_name: str
    receiver_id: int | None = Field(default=None, foreign_key="user.id")
    challenge_id: int | None = Field(default=None, foreign_key="challenge.id")
    challenge_name: str
    answer: bool | None = Field(default=None)
    created_at: date = Field(default_factory = date.today)

