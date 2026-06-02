from sqlmodel import SQLModel, Field
from datetime import datetime, UTC

class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    last_workout: datetime | None = Field(default=None)
    workout_count: int = Field(default=0)
    gym_registration: int = Field(foreign_key="gym.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    status: bool = Field(default=True)
