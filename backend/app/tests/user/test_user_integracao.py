# Criação de testes para o CRUD de User e seus validadores
import pytest

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