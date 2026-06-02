from sqlmodel import SQLModel, Field
from datetime import datetime, UTC

class User(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    unique_name: str = Field(unique=True)
    email: str = Field(unique=True)
    password: str
    xp: int = Field(default=0)
    last_workout: datetime | None = None
    streak: int = Field(default=0)
    best_streak: int = Field(default=0)
    role: str
    active: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    