from pyndatic import BaseModel
from datetime import datetime

class StudentCreateSchema(BaseModel):
    user_id: int

class StudentResponseSchema(BaseModel):
    model_config = {
        "from_attributes": True
    }
    
    id: int
    user_id: int
    last_workout: datetime | None
    workout_count: int

class StudentUpdateWorkoutSchema(BaseModel):
    id: int
    last_workout: datetime | None = None
    workout_count: int | None = None

