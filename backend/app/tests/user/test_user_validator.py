from fastapi import HTTPException
from app.validators.validate_user import validate_name, validate_password, validate_unique_name
import pytest

def test_validate_name():
    assert validate_name("Joao", "Silva") == True

def test_validate_first_name_number():
    with pytest.raises(HTTPException):
        validate_name("Joao123", "Silva")

def test_validate_last_name_number():
    with pytest.raises(HTTPException):
        validate_name("Joao", "Silva123")
    
def test_validate_first_name_empty():
    with pytest.raises(HTTPException):
        validate_name("", "Silva")

def test_validate_last_name_empty():
    with pytest.raises(HTTPException):
        validate_name("Joao", "")    

def test_validate_password():
    assert validate_password("senha123!") == True

#def test_validate_password_not_number():
#    with pytest.raises(HTTPException):
#        validate_password("abcde!")

#def test_validate_password_not_letter():
#    with pytest.raises(HTTPException):
#        validate_password("12345!")

#def test_validate_password_not_special_char():
#    with pytest.raises(HTTPException):
#        validate_password("senha1")    

#def test_validate_password_empty():
#    with pytest.raises(HTTPException):
#        validate_password("")

def test_validate_unique_name():
    assert validate_unique_name("joaosilva123") == True

def test_validate_unique_name_empty():
    with pytest.raises(HTTPException):
        validate_unique_name("")

def test_validate_unique_name_not_alphanumeric():
    with pytest.raises(HTTPException):
        validate_unique_name("joaosilva!@")
