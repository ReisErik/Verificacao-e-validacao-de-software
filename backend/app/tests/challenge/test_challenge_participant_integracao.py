from app.core.auth import get_current_user
from app.tests.conftest import override_get_current_user
from app.main import app
from datetime import datetime, UTC, timedelta
from app.models.challenge_invite import ChallengeInvite
from app.models.challenge_participant import ChallengeParticipant
from app.models.challenge_progress import ChallengeProgress
from app.models.challenge import Challenge
from app.utils.constantes import *

def test_join_challenge_accept(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user2"].id, session
    )

    start = datetime.now(UTC)
    end = start + timedelta(days=7)

    challenge = Challenge(
        id=1,
        owner=users["user1"].id,
        name="Teste",
        description="Teste",
        start_date=start,
        end_date=end,
        goal=5,
        xp_reward=100,
        visibility=True,
        category="Estudos",
        type_challenge="STREAK",
        mode_challenge="GROUP",
        max_participants = 5
    )

    participant = ChallengeParticipant(
        user_id=users["user1"].id,
        challenge_id=1,
    )

    progress = ChallengeProgress(
        challenge_id=1,
        user_id=users["user1"].id,
        current_progress=0,
        completed=False,
    )

    invite = ChallengeInvite(
        sender_id=users["user1"].id,
        sender_name="User One",
        receiver_id=users["user2"].id,
        receiver_name="teste",
        challenge_id=1,
        challenge_name="Teste",
        sent=True,
        answer=None,
    )

    session.add(challenge)
    session.add(participant)
    session.add(progress)
    session.add(invite)
    session.commit()
    session.refresh(invite)

    response = client.post(
        "/challenge/participant/join",
        json={
            "challenge_id": 1,
            "invite_id": invite.id,
            "answer": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["answer"] is True

    app.dependency_overrides.clear()

def test_join_challenge_refuse(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user2"].id, session
    )

    start = datetime.now(UTC)
    end = start + timedelta(days=7)
    
    challenge = Challenge(
        id=1,
        owner=users["user1"].id,
        name="Teste",
        description="Teste",
        start_date=start,
        end_date=end,
        goal=5,
        xp_reward=100,
        visibility=True,
        category="Estudos",
        type_challenge="STREAK",
        mode_challenge="GROUP",
        max_participants = 5
    )

    participant = ChallengeParticipant(
        user_id=users["user1"].id,
        challenge_id=1,
    )

    progress = ChallengeProgress(
        challenge_id=1,
        user_id=users["user1"].id,
        current_progress=0,
        completed=False,
    )

    invite = ChallengeInvite(
        sender_id=users["user1"].id,
        sender_name="User One",
        receiver_id=users["user2"].id,
        receiver_name="teste",
        challenge_id=1,
        challenge_name="Teste",
        sent=True,
        answer=None,
    )

    session.add(challenge)
    session.add(participant)
    session.add(progress)
    session.add(invite)
    session.commit()
    session.refresh(invite)

    response = client.post(
        "/challenge/participant/join",
        json={
            "challenge_id": 1,
            "invite_id": invite.id,
            "answer": False,
        },
    )

    assert response.status_code == 200
    assert response.json()["answer"] is False

    app.dependency_overrides.clear()

def test_get_challenge_participate(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user1"].id, session
    )

    participant = ChallengeParticipant(
        user_id=users["user1"].id,
        challenge_id=1,
    )

    session.add(participant)
    session.commit()

    response = client.get("/challenge/participant/get/1")

    assert response.status_code == 200
    assert response.json()["challenge_id"] == 1

    app.dependency_overrides.clear()

def test_get_all_challenge_participate(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user1"].id, session
    )

    start = datetime.now(UTC)
    end = start + timedelta(days=7)

    challenge = Challenge(
        id=1,
        owner=users["user1"].id,
        name="Teste",
        description="Teste",
        start_date=start,
        end_date=end,
        goal=5,
        xp_reward=100,
        visibility=True,
        category="Estudos",
        type_challenge="STREAK",
        mode_challenge="GROUP",
        max_participants = 5
    )

    participant = ChallengeParticipant(
        user_id=users["user1"].id,
        challenge_id=1,
    )

    session.add(challenge)
    session.add(participant)
    session.commit()
    session.refresh(participant)  

    response = client.get("/challenge/participant/get/all")

    assert response.status_code == 200
    assert len(response.json()) == 1

    app.dependency_overrides.clear()

def test_leave_challenge(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user1"].id, session
    )

    start = datetime.now(UTC)
    end = start + timedelta(days=7)

    challenge = Challenge(
        id=1,
        owner=users["user1"].id,
        name="Teste",
        description="Teste",
        start_date=start,
        end_date=end,
        goal=5,
        xp_reward=100,
        visibility=True,
        category="Estudos",
        type_challenge="STREAK",
        mode_challenge="GROUP",
        max_participants = 5
    )

    participant = ChallengeParticipant(
        user_id=users["user1"].id,
        challenge_id=1,
    )

    progress = ChallengeProgress(
        challenge_id=1,
        user_id=users["user1"].id,
        current_progress=0,
        completed=False,
    )

    session.add(challenge)
    session.add(participant)
    session.add(progress)
    session.commit()

    response = client.delete("/challenge/participant/leave/1")

    assert response.status_code == 200
    assert response.json()["message"] == "Usuario saiu do desafio"

    app.dependency_overrides.clear()

def test_join_fail_user_already_participant(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user2"].id, session
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
        xp_reward=100,
        visibility=True,
        category="Estudos",
        type_challenge="STREAK",
        mode_challenge="GROUP",
        max_participants=5,
    )

    session.add(challenge)
    session.commit()
    session.refresh(challenge)

    invite = ChallengeInvite(
        sender_id=users["user1"].id,
        sender_name="User One",
        receiver_id=users["user2"].id,
        receiver_name="teste",
        challenge_id=challenge.id,
        challenge_name=challenge.name,
        sent=True,
        answer=None,
    )

    session.add(invite)

    participant = ChallengeParticipant(
        user_id=users["user2"].id,
        challenge_id=challenge.id,
    )

    session.add(participant)
    session.commit()
    session.refresh(invite)

    response = client.post(
        "/challenge/participant/join",
        json={
            "challenge_id": challenge.id,
            "invite_id": invite.id,
            "answer": True,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Usuario já está participando do desafio"

    app.dependency_overrides.clear()

def test_join_fail_active_challenge_limit(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user2"].id, session
    )

    start = datetime.now(UTC)
    end = start + timedelta(days=10)

    challenge = Challenge(
        owner=users["user1"].id,
        name="Novo desafio",
        description="Teste",
        start_date=start,
        end_date=end,
        goal=5,
        xp_reward=100,
        visibility=True,
        category="Estudos",
        type_challenge="STREAK",
        mode_challenge="GROUP",
        max_participants=5,
    )

    session.add(challenge)
    session.commit()
    session.refresh(challenge)

    for i in range(MAX_ACTIVE_CHALLENGES):
        session.add(
            ChallengeProgress(
                challenge_id=1000 + i,
                user_id=users["user2"].id,
                current_progress=0,
                completed=False,
            )
        )

    invite = ChallengeInvite(
        sender_id=users["user1"].id,
        sender_name="User One",
        receiver_id=users["user2"].id,
        receiver_name="teste",
        challenge_id=challenge.id,
        challenge_name=challenge.name,
        sent=True,
        answer=None,
    )

    session.add(invite)
    session.commit()
    session.refresh(invite)

    response = client.post(
        "/challenge/participant/join",
        json={
            "challenge_id": challenge.id,
            "invite_id": invite.id,
            "answer": True,
        },
    )

    assert response.status_code == 400
    assert "limite" in response.json()["detail"].lower()

    app.dependency_overrides.clear()

def test_join_fail_participant_limit(client, session, users):
    app.dependency_overrides[get_current_user] = override_get_current_user(
        users["user2"].id, session
    )

    start = datetime.now(UTC)
    end = start + timedelta(days=10)

    challenge = Challenge(
        owner=users["user1"].id,
        name="Lotado",
        description="Teste",
        start_date=start,
        end_date=end,
        goal=5,
        xp_reward=100,
        visibility=True,
        category="Estudos",
        type_challenge="STREAK",
        mode_challenge="GROUP",
        max_participants=1,
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

    invite = ChallengeInvite(
        sender_id=users["user1"].id,
        sender_name="User One",
        receiver_id=users["user2"].id,
        receiver_name="teste",
        challenge_id=challenge.id,
        challenge_name=challenge.name,
        sent=True,
        answer=None,
    )

    session.add(invite)
    session.commit()
    session.refresh(invite)

    response = client.post(
        "/challenge/participant/join",
        json={
            "challenge_id": challenge.id,
            "invite_id": invite.id,
            "answer": True,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Desafio atingiu o limite de participantes"

    app.dependency_overrides.clear()