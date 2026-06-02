from pydantic import BaseModel,Field
from datetime import datetime

class GymCreateSchema(BaseModel):
    owner: int
    name: str = Field(max_length=20)
    location: str = Field(max_length=50)

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