from app.core.auth import get_current_user
from app.tests.conftest import override_get_current_user
from app.main import app
from datetime import datetime, UTC, timedelta
from sqlmodel import select
from app.models.challenge_progress import ChallengeProgress
from app.models.user import User

def test_get_progress(client, users, session):
    app.dependency_overrides[get_current_user] = override_get_current_user(users["user1"].id, session)

    payload = {
        "name": "Run",
        "description": "test",
        "start_date": "2026-01-01T00:00:00",
        "end_date": "2026-01-10T00:00:00",
        "goal": 5,
        "visibility": True,
        "category": "fitness",
        "type_challenge": "STREAK",
        "mode_challenge": "SOLO"
    }

    res = client.post("/challenge/create", json=payload)
    challenge_id = res.json()["id"]

    response = client.get(f"challenge/progress/get/{challenge_id}")

    assert response.status_code == 200, response.json()

    data = response.json()
    assert data["challenge_id"] == challenge_id

    app.dependency_overrides.clear()

def test_get_progress_not_found(client, users, session):
    app.dependency_overrides[get_current_user] = override_get_current_user(users["user1"].id, session)

    response = client.get("challenge/progress/get/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario não está participando deste desafio"

    app.dependency_overrides.clear()

def test_update_progress_streak(client, users, session):
    app.dependency_overrides[get_current_user] = override_get_current_user(users["user1"].id, session)

    start = datetime.now(UTC)
    end = datetime.now(UTC) + timedelta(days=10)

    payload = {
        "name": "Streak",
        "description": "test",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "goal": 3,
        "visibility": True,
        "category": "fitness",
        "type_challenge": "STREAK",
        "mode_challenge": "SOLO"
    }

    res = client.post("/challenge/create", json=payload)
    challenge_id = res.json()["id"]

    update_payload = {
        "challenge_id": challenge_id,
        "score": 1
    }

    response = client.patch("challenge/progress/update", json=update_payload)

    assert response.status_code == 200, response.json()

    data = response.json()
    assert data["current_progress"] == 1

    app.dependency_overrides.clear()

def test_update_progress_score(client, users, session):
    app.dependency_overrides[get_current_user] = override_get_current_user(users["user1"].id, session)

    start = datetime.now(UTC)
    end = datetime.now(UTC) + timedelta(days=10)

    payload = {
        "name": "Score challenge",
        "description": "test",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "goal": 100,
        "visibility": True,
        "category": "fitness",
        "type_challenge": "AMOUNT",
        "mode_challenge": "SOLO"
    }

    res = client.post("/challenge/create", json=payload)
    challenge_id = res.json()["id"]

    update_payload = {
        "challenge_id": challenge_id,
        "score": 10
    }

    response = client.patch("challenge/progress/update", json=update_payload)

    assert response.status_code == 200, response.json()

    data = response.json()
    assert data["current_progress"] == 10

    app.dependency_overrides.clear()

def test_update_progress_invalid_score(client, users, session):
    app.dependency_overrides[get_current_user] = override_get_current_user(users["user1"].id, session)

    start = datetime.now(UTC)
    end = datetime.now(UTC) + timedelta(days=10)

    payload = {
        "name": "Score test",
        "description": "test",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "goal": 100,
        "visibility": True,
        "category": "fitness",
        "type_challenge": "AMOUNT",
        "mode_challenge": "SOLO"
    }

    res = client.post("/challenge/create", json=payload)
    challenge_id = res.json()["id"]

    update_payload = {
        "challenge_id": challenge_id,
        "score": 0
    }

    response = client.patch("challenge/progress/update", json=update_payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Score precisa ser positivo"

    app.dependency_overrides.clear()

def create_challenge_payload(start, end):
    return {
        "name": "Finish fast",
        "description": "test",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "goal": 20,
        "visibility": True,
        "category": "fitness",
        "type_challenge": "AMOUNT",
        "mode_challenge": "SOLO"
    }

def test_completion_solo_reward(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user1"].id, session
    )

    start = datetime.now(UTC)
    end = start + timedelta(days=2)  

    payload = {
        "name": "Finish fast",
        "description": "test",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "goal": 3,
        "visibility": True,
        "category": "fitness",
        "type_challenge": "STREAK",
        "mode_challenge": "SOLO",
    }

    res = client.post("/challenge/create", json=payload)
    assert res.status_code == 200, res.json()

    challenge_id = res.json()["id"]

    r1 = client.patch(
        "/challenge/progress/update",
        json={
            "challenge_id": challenge_id,
            "score": 1,
        },
    )

    assert r1.status_code == 200, r1.json()
    assert r1.json()["completed"] is False

    progression = session.exec(
        select(ChallengeProgress).where(
            ChallengeProgress.challenge_id == challenge_id,
            ChallengeProgress.user_id == users["user1"].id,
        )
    ).first()

    progression.last_update -= timedelta(days=1)
    session.add(progression)
    session.commit()

    r2 = client.patch(
        "/challenge/progress/update",
        json={
            "challenge_id": challenge_id,
            "score": 1,
        },
    )

    progression.last_update -= timedelta(days=1)
    session.add(progression)
    session.commit()

    r3 = client.patch(
        "/challenge/progress/update",
        json={
            "challenge_id": challenge_id,
            "score": 1,
        },
    )

    assert r3.status_code == 200, r3.json()

    data = r3.json()

    assert data["completed"] is True
    fresh_user = session.get(User, users["user1"].id)
    assert fresh_user.xp > 0

    app.dependency_overrides.clear()