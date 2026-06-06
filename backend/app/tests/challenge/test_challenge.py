import pytest
from fastapi import HTTPException
from unittest.mock import Mock, patch
from datetime import datetime, timedelta, UTC

from app.services.challenge_service import create_challenge, get_challenge_or_404
from app.schemas.challenge_schema import CreateChallengeSchema

@pytest.fixture(autouse=True)
def mock_auth():
    with patch("app.services.challenge_service.validateAuth"):
        yield

def test_create_challenge_success():
    session = Mock()

    current_user = Mock()
    current_user.id = 1

    data = CreateChallengeSchema(
        name="Desafio teste",
        description="Teste",
        xp_reward=100,
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=7),
        goal=200,
        visibility=False,
        type_challenge="TIME"
    )

    result = create_challenge(data, session, current_user)

    session.flush.assert_called_once()
    session.commit.assert_called_once()

    assert result.owner == 1
    assert result.name == "Desafio teste"
    assert result.goal == 200

def test_create_challenge_invalid_date():
    session = Mock()

    current_user = Mock()
    current_user.id = 1

    data = CreateChallengeSchema(
        name="Desafio teste",
        description="Teste",
        xp_reward=100,
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) - timedelta(days=1),
        goal=200,
        visibility=False,
        type_challenge="TIME"
    )

    with pytest.raises(HTTPException) as e: 
        create_challenge(data, session, current_user)

    assert e.value.status_code == 400
    assert e.value.detail == "Data final deve ser maior que a inicial."

def test_get_challenge_or_404_find():
    session = Mock()
    current_user = Mock()
    challenge = Mock()
    challenge.id = 1

    session.get.return_value = challenge
    result = get_challenge_or_404(challenge.id, session, current_user)
    session.get.assert_called_once()

    assert result.id == challenge.id

def test_get_challenge_or_404_not_found():
    session = Mock()
    current_user = Mock()
    challenge = Mock()
    challenge.id = 1

    session.get.return_value = None

    with pytest.raises(HTTPException) as e:
        get_challenge_or_404(challenge.id, session, current_user)
   
    session.get.assert_called_once()

    assert e.value.status_code == 404
    assert e.value.detail == "Desafio não encontrado"

