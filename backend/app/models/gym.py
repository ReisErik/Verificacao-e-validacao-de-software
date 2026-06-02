from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from user import User

class Gym(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    owner: int = Field(foreign_key="user.id")
    name: str
    location: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))