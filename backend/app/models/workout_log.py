from sqlmodel import SQLModel, Field
from datetime import datetime

class WorkoutLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_user : int = Field(default=None, foreign_key="user.id")
    workout_date : datetime
    duration : int | None = None
    description : str | None = Field(default=None, max_length=100)