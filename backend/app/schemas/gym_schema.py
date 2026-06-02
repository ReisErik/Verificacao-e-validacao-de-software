from pydantic import BaseModel
from datetime import datetime

class GymCreateSchema(BaseModel):
    owner: int
    name: str
    location: str

class GymResponseSchema(BaseModel):
    model_config = {
        "from_attributes": True
    }
    
    id: int
    owner: int
    name: str
    location: str
    total_students: int
    created_at: datetime
    updated_at: datetime