from sqlmodel import SQLModel, Field
from datetime import datetime

class Challenge(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    xp_reward: int
    start_date: datetime
    end_date: datetime
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
