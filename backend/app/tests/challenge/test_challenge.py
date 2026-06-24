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

def test_create_challenge_streak_success():
    session = Mock()

    current_user = Mock()
    current_user.id = 1

    data = CreateChallengeSchema(
        name="Desafio teste",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=7),
        goal=5,
        visibility=False,
        type_challenge="STREAK",
        category="Estudos",
        mode_challenge="SOLO"
    )

    result = create_challenge(data, session, current_user)

    session.flush.assert_called_once()
    session.commit.assert_called_once()

    assert result.owner == 1
    assert result.name == "Desafio teste"
    assert result.goal == 5

def test_create_challenge_streak_limits():
    session = Mock()

    current_user = Mock()
    current_user.id = 1

    dataLimitUpper = CreateChallengeSchema(
        name="Teste Limite Superior",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=30),
        goal=30,
        visibility=False,
        type_challenge="STREAK",
        category="Estudos",
        mode_challenge="SOLO"
    )

    dataLimitBottom = CreateChallengeSchema(
        name="Teste Limite Inferior",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=7),
        goal=3,
        visibility=False,
        type_challenge="STREAK",
        category="Estudos",
        mode_challenge="SOLO"
    )

    resultUpper = create_challenge(dataLimitUpper,session,current_user)
    resultBottom = create_challenge(dataLimitBottom,session, current_user)

    assert resultUpper.name == "Teste Limite Superior"
    assert resultBottom.name == "Teste Limite Inferior"

def test_create_challenge_time_success():
    session = Mock()

    current_user = Mock()
    current_user.id = 1

    data = CreateChallengeSchema(
        name="Desafio teste",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=7),
        goal=14,
        visibility=False,
        type_challenge="TIME",
        category="Estudos",
        mode_challenge="SOLO"
    )

    result = create_challenge(data, session, current_user)

    session.flush.assert_called_once()
    session.commit.assert_called_once()

    assert result.owner == 1
    assert result.name == "Desafio teste"
    assert result.goal == 14

def test_create_challenge_time_limits():
    session = Mock()

    current_user = Mock()
    current_user.id = 1

    dataLimitUpper = CreateChallengeSchema(
        name="Teste Limite Superior",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=6),
        goal=21,
        visibility=False,
        type_challenge="TIME",
        category="Estudos",
        mode_challenge="SOLO"
    )

    dataLimitBottom = CreateChallengeSchema(
        name="Teste Limite Inferior",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=3),
        goal=1,
        visibility=False,
        type_challenge="TIME",
        category="Estudos",
        mode_challenge="SOLO"
    )

    resultUpper = create_challenge(dataLimitUpper,session,current_user)
    resultBottom = create_challenge(dataLimitBottom,session, current_user)

    assert resultUpper.name == "Teste Limite Superior"
    assert resultBottom.name == "Teste Limite Inferior"

def test_create_challenge_amount_success():
    session = Mock()

    current_user = Mock()
    current_user.id = 1

    data = CreateChallengeSchema(
        name="Desafio teste",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=7),
        goal=100,
        visibility=False,
        type_challenge="AMOUNT",
        category="Estudos",
        mode_challenge="SOLO"
    )

    result = create_challenge(data, session, current_user)

    session.flush.assert_called_once()
    session.commit.assert_called_once()

    assert result.owner == 1
    assert result.name == "Desafio teste"
    assert result.goal == 100

def test_create_challenge_amount_limits():
    session = Mock()

    current_user = Mock()
    current_user.id = 1

    dataLimitUpper = CreateChallengeSchema(
        name="Teste Limite Superior",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=6),
        goal=140,
        visibility=False,
        type_challenge="AMOUNT",
        category="Estudos",
        mode_challenge="SOLO"
    )

    dataLimitBottom = CreateChallengeSchema(
        name="Teste Limite Inferior",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=6),
        goal=7,
        visibility=False,
        type_challenge="AMOUNT",
        category="Estudos",
        mode_challenge="SOLO"
    )

    resultUpper = create_challenge(dataLimitUpper,session,current_user)
    resultBottom = create_challenge(dataLimitBottom,session, current_user)

    assert resultUpper.name == "Teste Limite Superior"
    assert resultBottom.name == "Teste Limite Inferior"

def test_create_challenge_streak_more_duration():
    session = Mock()

    current_user = Mock()
    current_user.id = 1

    data = CreateChallengeSchema(
        name="Desafio teste",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=6),
        goal=8,
        visibility=False,
        type_challenge="STREAK",
        category="Estudos",
        mode_challenge="SOLO"
    )

    with pytest.raises(HTTPException) as e:
        create_challenge(data, session, current_user)
    
    assert e.value.status_code == 400
    assert e.value.detail == "Desafios STREAK não podem ter meta maior que a duração."

def test_create_challenge_streak_more_30_days():
    session = Mock()

    current_user = Mock()
    current_user.id = 1

    data = CreateChallengeSchema(
        name="Desafio teste",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=31),
        goal=31,
        visibility=False,
        type_challenge="STREAK",
        category="Estudos",
        mode_challenge="SOLO"
    )
    
    with pytest.raises(HTTPException) as e:
        create_challenge(data, session, current_user)
    
    assert e.value.status_code == 400
    assert e.value.detail == "Desafios STREAK podem ter no máximo 30 dias."

def test_create_challenge_streak_less_3_days():
    session = Mock()

    current_user = Mock()
    current_user.id = 1

    data = CreateChallengeSchema(
        name="Desafio teste",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=7),
        goal=2,
        visibility=False,
        type_challenge="STREAK",
        category="Estudos",
        mode_challenge="SOLO"
    )
    
    with pytest.raises(HTTPException) as e:
        create_challenge(data, session, current_user)
    
    assert e.value.status_code == 400
    assert e.value.detail == "Desafios Streak precisam ter no mínimo 3 dias"

def test_create_challenge_time_more_3_hours_days():
    session = Mock()

    current_user = Mock()
    current_user.id = 1

    data = CreateChallengeSchema(
        name="Desafio teste",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=6),
        goal=22,
        visibility=False,
        type_challenge="TIME",
        category="Estudos",
        mode_challenge="SOLO"
    )

    with pytest.raises(HTTPException) as e:
        create_challenge(data, session, current_user)
    
    assert e.value.status_code == 400
    assert e.value.detail == "Desafios TIME não podem exigir mais de 3 horas por dia."

def test_create_challenge_time_less_15_minutes_days():
    session = Mock()

    current_user = Mock()
    current_user.id = 1

    data = CreateChallengeSchema(
        name="Desafio teste",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=9),
        goal=2,
        visibility=False,
        type_challenge="TIME",
        category="Estudos",
        mode_challenge="SOLO"
    )

    with pytest.raises(HTTPException) as e:
        create_challenge(data, session, current_user)
    
    assert e.value.status_code == 400
    assert e.value.detail == "Desafios TIME precisam ter pelo menos 15 minutos por dia."

def test_create_challenge_amount_more_20_units_days():
    session = Mock()

    current_user = Mock()
    current_user.id = 1

    data = CreateChallengeSchema(
        name="Desafio teste",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=6),
        goal=141,
        visibility=False,
        type_challenge="AMOUNT",
        category="Estudos",
        mode_challenge="SOLO"
    )

    with pytest.raises(HTTPException) as e:
        create_challenge(data, session, current_user)
    
    assert e.value.status_code == 400
    assert e.value.detail == "Desafios AMOUNT não podem exigir mais de 20 unidades por dia."

def test_create_challenge_amount_less_1_unit_days():
    session = Mock()

    current_user = Mock()
    current_user.id = 1

    data = CreateChallengeSchema(
        name="Desafio teste",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) + timedelta(days=7),
        goal=6,
        visibility=False,
        type_challenge="AMOUNT",
        category="Estudos",
        mode_challenge="SOLO"
    )

    with pytest.raises(HTTPException) as e:
        create_challenge(data, session, current_user)
    
    assert e.value.status_code == 400
    assert e.value.detail == "Desafios AMOUNT precisam ter pelo menos 1 unidade por dia."

def test_create_challenge_invalid_date():
    session = Mock()

    current_user = Mock()
    current_user.id = 1

    data = CreateChallengeSchema(
        name="Desafio teste",
        description="Teste",
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC) - timedelta(days=1),
        goal=14,
        visibility=False,
        type_challenge="TIME",
        category="Estudos",
        mode_challenge="SOLO"
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

