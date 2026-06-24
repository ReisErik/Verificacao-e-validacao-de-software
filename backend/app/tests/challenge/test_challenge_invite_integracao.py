from app.main import app
from datetime import datetime, UTC, timedelta
from app.core.auth import get_current_user
from app.tests.conftest import override_get_current_user
from app.models.challenge_invite import ChallengeInvite

def test_send_invite(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user1"].id, session
    )

    start = datetime.now(UTC)
    end = start + timedelta(days=7)

    challenge = client.post(
        "/challenge/create",
        json={
            "name": "Invite Test",
            "description": "test",
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "goal": 7,
            "visibility": True,
            "category": "Estudos",
            "type_challenge": "STREAK",
            "mode_challenge": "GROUP",
        },
    )

    challenge_id = challenge.json()["id"]

    response = client.post(
        f"/challenge/invite/send/{challenge_id}/{users['user2'].id}"
    )

    assert response.status_code == 200

    app.dependency_overrides.clear()

def test_get_invite(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user1"].id, session
    )

    invite = ChallengeInvite(
        sender_id=users["user1"].id,
        sender_name="User One",
        receiver_id=users["user2"].id,
        challenge_id=1,
        challenge_name="Teste",
        sent=True,
    )

    session.add(invite)
    session.commit()
    session.refresh(invite)

    response = client.get(
        f"/challenge/invite/get/{invite.id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == invite.id

    app.dependency_overrides.clear()

def test_cancel_invite(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user1"].id, session
    )

    invite = ChallengeInvite(
        sender_id=users["user1"].id,
        sender_name="User One",
        receiver_id=users["user2"].id,
        challenge_id=1,
        challenge_name="Teste",
        sent=True,
        answer=False,
    )

    session.add(invite)
    session.commit()
    session.refresh(invite)

    response = client.delete(
        f"/challenge/invite/cancel/{invite.id}/{users['user2'].id}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Convite cancelado"

    app.dependency_overrides.clear()

def test_get_sent_invites(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user1"].id, session
    )

    invite = ChallengeInvite(
        sender_id=users["user1"].id,
        sender_name="User One",
        receiver_id=users["user2"].id,
        challenge_id=1,
        challenge_name="Teste",
        sent=True,
    )

    session.add(invite)
    session.commit()

    response = client.get("/challenge/invite/sent")

    assert response.status_code == 200
    assert len(response.json()) == 1

    app.dependency_overrides.clear()

def test_get_received_invites(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user2"].id, session
    )

    invite = ChallengeInvite(
        sender_id=users["user1"].id,
        sender_name="User One",
        receiver_id=users["user2"].id,
        challenge_id=1,
        challenge_name="Teste",
        sent=True,
    )

    session.add(invite)
    session.commit()

    response = client.get("/challenge/invite/received")

    assert response.status_code == 200
    assert len(response.json()) == 1

    app.dependency_overrides.clear()