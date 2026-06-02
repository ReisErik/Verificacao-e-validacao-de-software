from pydantic import BaseModel

class StudentMatriculateCreateSchema(BaseModel):
    student_id: int
    gym_id: int

class StudentMatriculateResponseSchema(BaseModel):
    model_config = {
        "from_attributes": True
    }
    
    id: int
    student_id: int
    gym_id: int
    num_matriculate: int
    status: bool