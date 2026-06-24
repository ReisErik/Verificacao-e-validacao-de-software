import pytest
from app.core.auth import get_current_user
from app.tests.conftest import override_get_current_user
from app.main import app

def test_create_challenge(client, users, session):
    app.dependency_overrides[get_current_user] = override_get_current_user(users["user1"].id, session)

    payload = {
        "name": "teste",
        "description": "teste",
        "start_date": "2026-01-01T00:00:00",
        "end_date": "2026-01-10T00:00:00",
        "goal": 8,
        "visibility": True,
        "category": "Estudo",
        "type_challenge": "STREAK",
        "mode_challenge": "SOLO", 
        "max_participants":5
    }

    response = client.post("/challenge/create", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "teste"
    assert data["goal"] == 8
    assert "id" in data

    app.dependency_overrides.clear()

def test_get_all_challenges(client, users, session):
    app.dependency_overrides[get_current_user] = override_get_current_user(users["user1"].id, session)

    payload = {
        "name": "teste",
        "description": "teste",
        "start_date": "2026-01-01T00:00:00",
        "end_date": "2026-01-10T00:00:00",
        "goal": 5,
        "visibility": True,
        "category": "Estudo",
        "type_challenge": "STREAK",
        "mode_challenge": "SOLO", 
        "max_participants":5
    }

    client.post("/challenge/create", json=payload)

    response = client.get("/challenge/all")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    app.dependency_overrides.clear()

def test_get_challenge_by_id(client, users, session):
    app.dependency_overrides[get_current_user] = override_get_current_user(users["user1"].id, session)

    payload = {
        "name": "Find Me",
        "description": "test",
        "start_date": "2026-01-01T00:00:00",
        "end_date": "2026-01-10T00:00:00",
        "goal": 5,
        "visibility": True,
        "category": "Estudo",
        "type_challenge": "STREAK",
        "mode_challenge": "SOLO", 
        "max_participants":5
    }

    res = client.post("/challenge/create", json=payload)
    challenge_id = res.json()["id"]

    response = client.get(f"/challenge/{challenge_id}")

    assert response.status_code == 200
    assert response.json()["id"] == challenge_id

    app.dependency_overrides.clear()

def test_get_challenge_not_found(client, users, session):
    app.dependency_overrides[get_current_user] = override_get_current_user(users["user1"].id, session)

    response = client.get("/challenge/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Desafio não encontrado"

    app.dependency_overrides.clear()

def test_multi_user_challenges(client, users,session):
    app.dependency_overrides[get_current_user] = override_get_current_user(users["user1"].id, session)

    payload = {
        "name": "teste",
        "description": "teste",
        "start_date": "2026-01-01T00:00:00",
        "end_date": "2026-01-10T00:00:00",
        "goal": 5,
        "visibility": True,
        "category": "Estudo",
        "type_challenge": "STREAK",
        "mode_challenge": "SOLO", 
        "max_participants": 5
    }

    res = client.post("/challenge/create", json=payload)
    challenge_id = res.json()["id"]

    app.dependency_overrides[get_current_user] = override_get_current_user(users["user2"].id, session)

    response = client.get(f"/challenge/{challenge_id}")

    assert response.status_code in [200, 403, 404]

    app.dependency_overrides.clear()