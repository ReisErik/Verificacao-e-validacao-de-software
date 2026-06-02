from sqlmodel import SQLModel, Field

class StudentMatriculate(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    gym_id: int = Field(foreign_key="gym.id")
    num_matriculate: int 
    status: bool = Field(default=True)