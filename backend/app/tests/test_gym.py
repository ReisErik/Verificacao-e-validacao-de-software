# gym right -> true
# gym name is not string -> false
# gym location is not string -> false
# gym owner is not int -> false
# gym schema -> true


import pytest
from app.validators.validate_gym import validate_gym
from fastapi import HTTPException
from pydantic import ValidationError
from app.schemas.gym_schema import GymCreateSchema

def test_validate_gym():
    assert validate_gym("Gym", "Location", 1) == True

def test_validate_gym_name_empty():
    with pytest.raises(HTTPException):
        validate_gym("", "Location", 1)

def test_validate_gym_location_empty():
    with pytest.raises(HTTPException):
        validate_gym("Gym", "", 1)

def test_validate_gym_owner_id_none():
    with pytest.raises(HTTPException):
        validate_gym("Gym", "Location", None)

def test_validate_gym_name_not_alphanumeric():
    with pytest.raises(HTTPException):
        validate_gym("Gym!", "Location", 1)

def test_validate_gym_location_not_alphanumeric():
    with pytest.raises(HTTPException):
        validate_gym("Gym", "Location!", 1)

def test_validate_gym_name_not_string():
    with pytest.raises(ValidationError):
        GymCreateSchema(owner=1, name=1, location="Location")

def test_validate_gym_location_not_string():
    with pytest.raises(ValidationError):
        GymCreateSchema(owner=1, name="Gym", location=1)

def test_validate_gym_owner_not_int():
    with pytest.raises(ValidationError):
        GymCreateSchema(owner="a", name="Gym", location="Location")

def test_gym_schema():
    data = {
        "owner": 1,
        "name": "Gym",
        "location": "Location"
    }
    gym_schema = GymCreateSchema(**data)
    assert gym_schema.model_dump() == data

    data = {
        "owner": 1,
        "name": "G"*20,
        "location": "Location"
    }
    gym_schema = GymCreateSchema(**data)
    assert gym_schema.model_dump() == data

    data = {
        "owner": 1,
        "name": "Gym",
        "location": "L"*20
    }
    gym_schema = GymCreateSchema(**data)
    assert gym_schema.model_dump() == data


def test_gym_schema_name_long():
    data = {
        "owner": 1,
        "name": "G" * 21,
        "location": "Location"
    }
    with pytest.raises(ValidationError):
        GymCreateSchema(**data)

def test_gym_schema_location_long():
    data = {
        "owner": 1,
        "name": "Gym",
        "location": "L" * 51
    }
    with pytest.raises(ValidationError):
        GymCreateSchema(**data)