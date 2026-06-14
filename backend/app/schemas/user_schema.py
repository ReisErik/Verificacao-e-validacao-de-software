from pydantic import BaseModel, Field, EmailStr
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserCreateSchema(BaseModel):
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    unique_name: str = Field(max_length=20)
    email: EmailStr 
    password: str = Field(min_length=4, max_length=20)
    role: UserRole = UserRole.USER

class UserResponseSchema(BaseModel):
    model_config = {
        "from_attributes": True
    }
    
    id: int
    first_name: str
    last_name: str
    unique_name: str
    email: EmailStr
    role: UserRole
    active: bool

class UserUpdatePasswordSchema(BaseModel):
    new_password: str = Field(min_length=6, max_length=20)