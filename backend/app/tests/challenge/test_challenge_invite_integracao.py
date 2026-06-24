from app.main import app
from datetime import datetime, UTC, timedelta
from app.core.auth import get_current_user
from app.tests.conftest import override_get_current_user
from app.models.challenge_invite import ChallengeInvite
from app.models.challenge_participant import ChallengeParticipant
from app.models.challenge import Challenge

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
            "max_participants":5
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

def test_invite_fail_user_already_participant(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user1"].id, session
    )

    start = datetime.now(UTC)
    end = start + timedelta(days=10)

    challenge = Challenge(
        owner=users["user1"].id,
        name="Teste",
        description="Teste",
        start_date=start,
        end_date=end,
        goal=5,
        visibility=True,
        category="Estudos",
        type_challenge="STREAK",
        mode_challenge="GROUP",
        max_participants=5,
        xp_reward=100
    )

    session.add(challenge)
    session.commit()
    session.refresh(challenge)

    participant = ChallengeParticipant(
        user_id=users["user2"].id,
        challenge_id=challenge.id,
    )

    session.add(participant)
    session.commit()

    response = client.post(
        f"/challenge/invite/send/{challenge.id}/{users['user2'].id}"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Usuario já está participando do desafio"

    app.dependency_overrides.clear()

def test_invite_fail_challenge_full(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user1"].id, session
    )

    start = datetime.now(UTC)
    end = start + timedelta(days=10)

    challenge = Challenge(
        owner=users["user1"].id,
        name="Teste",
        description="Teste",
        start_date=start,
        end_date=end,
        goal=5,
        visibility=True,
        category="Estudos",
        type_challenge="STREAK",
        mode_challenge="GROUP",
        max_participants=1,
        xp_reward=100
    )

    session.add(challenge)
    session.commit()
    session.refresh(challenge)

    session.add(
        ChallengeParticipant(
            user_id=users["user1"].id,
            challenge_id=challenge.id,
        )
    )
    session.commit()

    response = client.post(
        f"/challenge/invite/send/{challenge.id}/{users['user2'].id}"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Desafio atingiu o limite de participantes"

    app.dependency_overrides.clear()

def test_invite_success_when_slot_available(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user1"].id, session
    )

    start = datetime.now(UTC)
    end = start + timedelta(days=10)

    challenge = Challenge(
        owner=users["user1"].id,
        name="Teste",
        description="Teste",
        start_date=start,
        end_date=end,
        goal=5,
        visibility=True,
        category="Estudos",
        type_challenge="STREAK",
        mode_challenge="GROUP",
        max_participants=5,
        xp_reward=100
    )

    session.add(challenge)
    session.commit()
    session.refresh(challenge)

    response = client.post(
        f"/challenge/invite/send/{challenge.id}/{users['user2'].id}"
    )

    assert response.status_code == 200

    data = response.json()
    assert data["receiver_id"] == users["user2"].id
    assert data["challenge_id"] == challenge.id

    app.dependency_overrides.clear()