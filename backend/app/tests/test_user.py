# Criação de testes para o CRUD de User e seus validadores
import pytest
from app.validators.validate_name import validate_name
from app.validators.validate_password import validate_password
from app.validators.validate_unique_name import validate_unique_name
from fastapi import HTTPException

# Testes unitários para os validadores

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

def test_validate_password_not_number():
    with pytest.raises(HTTPException):
        validate_password("abcde!")

def test_validate_password_not_letter():
    with pytest.raises(HTTPException):
        validate_password("12345!")

def test_validate_password_not_special_char():
    with pytest.raises(HTTPException):
        validate_password("senha1")    

def test_validate_password_empty():
    with pytest.raises(HTTPException):
        validate_password("")

def test_validate_unique_name():
    assert validate_unique_name("joaosilva123") == True

def test_validate_unique_name_empty():
    with pytest.raises(HTTPException):
        validate_unique_name("")

def test_validate_unique_name_not_alphanumeric():
    with pytest.raises(HTTPException):
        validate_unique_name("joaosilva!@")

# Testes de integração, requisiçoes HTTP para as rotas de usuário

def create_user_test(client, data):
    response = client.post("/user", json=data)

    print(response.status_code)
    print(response.json())

    return response.json()
    
def test_create_user(client):
    response = client.post("/user", json={
        "first_name": "Joao",
        "last_name": "Silva",
        "unique_name": "joaosilva",
        "email": "joao.silva@gmail.com",
        "password": "senha123!",
        "role": "user"
    })
    assert response.status_code == 200

def test_get_user(client):
    user = create_user_test(client, {
        "first_name": "Joao",
        "last_name": "Silva",
        "unique_name": "joaosilva1",
        "email": "joao.silva1@gmail.com",
        "password": "senha123!",
        "role": "user"
    })
    response = client.get(f"/user/{user['id']}")
    assert response.status_code == 200

def test_update_user_password(client):
    user = create_user_test(client, {
        "first_name": "Joao",
        "last_name": "Silva",
        "unique_name": "joaosilva2",
        "email": "joao.silva2@gmail.com",
        "password": "senha123!",
        "role": "user"
    })
    response = client.put(f"/user/{user['id']}/password", json={
        "new_password": "senha1234!"
    })
    assert response.status_code == 200

def test_delete_user(client):
    user = create_user_test(client, {
        "first_name": "Joao",
        "last_name": "Silva",
        "unique_name": "joaosilva3",
        "email": "joao.silva3@gmail.com",
        "password": "senha123!",
        "role": "user"
    })
    response = client.delete(f"/user/{user['id']}/delete")
    assert response.status_code == 204

def test_disable_user(client):
    user = create_user_test(client, {
        "first_name": "Joao",
        "last_name": "Silva",
        "unique_name": "joaosilva4",
        "email": "joao.silva4@gmail.com",
        "password": "senha123!",
        "role": "user"
    })
    response = client.post(f"/user/{user['id']}/disable")
    assert response.status_code == 200