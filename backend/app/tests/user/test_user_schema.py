import pytest
from app.schemas.user_schema import UserCreateSchema
from pydantic import ValidationError

def test_user_create_schema():
    data = {
        "first_name": "Joao",
        "last_name": "Silva",
        "unique_name": "joaosilva",
        "email": "joao.silva@gmail.com",
        "password": "senha123!",
        "role": "user"
    }
    user_schema = UserCreateSchema(**data)
    assert user_schema.model_dump() == data

def test_user_create_schema_invalid_email():
    data = {
        "first_name": "Joao",
        "last_name": "Silva",
        "unique_name": "joaosilva",
        "email": "joao.silva",
        "password": "senha123!",
        "role": "user"
    }
    with pytest.raises(ValidationError):
        UserCreateSchema(**data)

def test_user_create_schema_password_short():
    data = {
        "first_name": "Joao",
        "last_name": "Silva",
        "unique_name": "joaosilva",
        "email": "joao.silva@gmail.com",
        "password": "senha",
        "role": "user"
    }
    with pytest.raises(ValidationError):
        UserCreateSchema(**data)

def test_user_create_schema_password_long():
    data = {
        "first_name": "Joao",
        "last_name": "Silva",
        "unique_name": "joaosilva",
        "email": "joao.silva@gmail.com",
        "password": "a"*21,
        "role": "user"
    }
    with pytest.raises(ValidationError):
        UserCreateSchema(**data)

def test_user_create_schema_first_name_long():
    data = {
        "first_name": "a"*21,
        "last_name": "Silva",
        "unique_name": "joaosilva",
        "email": "joao.silva@gmail.com",
        "password": "senha123!",
        "role": "user"
    }
    with pytest.raises(ValidationError):
        UserCreateSchema(**data)

def test_user_create_schema_last_name_long():
    data = {
        "first_name": "Joao",
        "last_name": "a"*21,
        "unique_name": "joaosilva",
        "email": "joao.silva@gmail.com",
        "password": "senha123!",
        "role": "user"
    }
    with pytest.raises(ValidationError):
        UserCreateSchema(**data)

def test_user_create_schema_unique_name_long():
    data = {
        "first_name": "Joao",
        "last_name": "Silva",
        "unique_name": "a"*21,
        "email": "joao.silva@gmail.com",
        "password": "senha123!",
        "role": "user"
    }
    with pytest.raises(ValidationError):
        UserCreateSchema(**data)

def test_user_create_schema_role_invalid():
    data = {
        "first_name": "Joao",
        "last_name": "Silva",
        "unique_name": "joaosilva",
        "email": "joao.silva@gmail.com",
        "password": "senha123!",
        "role": "invalid_role"
    }
    with pytest.raises(ValidationError):
        UserCreateSchema(**data)