from sqlmodel import SQLModel, Field

class ChallengeInvite(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sender_id: int | None = Field(default=None, foreign_key="user.id")
    receiver_id: int | None = Field(default=None, foreign_key="user.id")
    challenge_id: int | None = Field(default=None, foreign_key="challenge.id")
    sent: bool = False
    answer: bool = None
