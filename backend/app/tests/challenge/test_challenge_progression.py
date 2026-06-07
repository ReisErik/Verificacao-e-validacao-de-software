import pytest
from unittest.mock import Mock, patch
from app.validators.validate_auth import validateAuth
from app.services.challenge_progression_service import get_progress_or_404, update_progress
from app.models.challenge_progress import ChallengeProgress
from app.schemas.challenge_schema import ProgressResponseSchema, ChallengeResponseSchema, UpdateProgressSchema
from fastapi import HTTPException
from datetime import datetime, UTC, timedelta

def test_get_progress_success():
    """Sucesso: Retorna o progresso do desafio"""
    session = Mock()
    current_user = Mock()
    current_user.id = 1
    progress = Mock()

    session.exec.return_value.first.return_value = progress
    result = get_progress_or_404(1, session, current_user)
    session.exec.assert_called_once()

    assert result is progress

def test_get_progress_not_found():
    """Erro: Progresso não encontrado"""
    session = Mock()
    current_user = Mock()
    
    session.exec.return_value.first.return_value = None

    with pytest.raises(HTTPException) as e:
        get_progress_or_404(1, session, current_user)
    
    session.exec.assert_called_once()
    assert e.value.status_code == 404
    assert e.value.detail == "Usuario não está participando deste desafio"

@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_success(progress_mock, challenge_mock):
    """Sucesso: Atualizou progresso do desafio, finalizou e adicionou XP"""
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 1900
    progress.completed = False

    challenge = Mock()
    challenge.id = 1
    challenge.xp_reward = 100
    challenge.goal = 2000
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=1)

    data = UpdateProgressSchema(
        challenge_id=1,
        score=200
    )

    progress_mock.return_value = progress
    challenge_mock.return_value = challenge

    response = update_progress(data, session, current_user)

    session.commit.assert_called_once()
    session.refresh.assert_called_with(progress)

    assert response.current_progress == 2000
    assert response.completed is True

    assert current_user.xp == 100

    session.add.assert_any_call(progress)
    session.add.assert_any_call(current_user)

@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_partial_progress(progress_mock, challenge_mock):
    """Sucesso: Atualizou progresso do desafio mas não completou"""
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 1000
    progress.completed = False

    challenge = Mock()
    challenge.id = 1
    challenge.goal = 2000
    challenge.xp_reward = 100
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=1)

    data = UpdateProgressSchema(
        challenge_id=1,
        score=200
    )

    progress_mock.return_value = progress
    challenge_mock.return_value = challenge

    response = update_progress(data, session, current_user)

    assert progress.current_progress == 1200
    assert progress.completed is False
    assert response.current_progress == 1200
    assert response.completed is False
    assert current_user.xp == 0

    session.commit.assert_called_once()

@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_challenge_not_started(progress_mock, challenge_mock):
    """Erro: Desafio não começou"""
    session = Mock()
    current_user = Mock()

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 1000
    progress.completed = False

    challenge = Mock()
    challenge.id = 1
    challenge.goal = 2000
    challenge.xp_reward = 100
    challenge.start_date = datetime.now(UTC) + timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=1)

    data = UpdateProgressSchema(
        challenge_id = 1,
        score = 200
    )

    progress_mock.return_value = progress
    challenge_mock.return_value = challenge

    with pytest.raises(HTTPException) as e:
        update_progress(data, session, current_user)
    
    assert e.value.status_code == 400
    assert e.value.detail == "Desafio ainda não começou"

@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_challenge_finished(progress_mock, challenge_mock):
    """Erro: Desafio já terminou"""
    session = Mock()
    current_user = Mock()

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 1000
    progress.completed = False

    challenge = Mock()
    challenge.id = 1
    challenge.goal = 2000
    challenge.xp_reward = 100
    challenge.start_date = datetime.now(UTC) - timedelta(days=2)
    challenge.end_date = datetime.now(UTC) - timedelta(days=1)

    data = UpdateProgressSchema(
        challenge_id = 1,
        score = 200
    )

    progress_mock.return_value = progress
    challenge_mock.return_value = challenge

    with pytest.raises(HTTPException) as e:
        update_progress(data, session, current_user)
    
    assert e.value.status_code == 400
    assert e.value.detail == "Desafio já acabou"

@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_challenge_score_negative(progress_mock, challenge_mock):
    """Erro: Score não pode ser negativo"""
    session = Mock()
    current_user = Mock()

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 1000
    progress.completed = False

    challenge = Mock()
    challenge.id = 1
    challenge.goal = 2000
    challenge.xp_reward = 100
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=1)

    data = UpdateProgressSchema(
        challenge_id = 1,
        score = -200
    )

    progress_mock.return_value = progress
    challenge_mock.return_value = challenge

    with pytest.raises(HTTPException) as e:
        update_progress(data, session, current_user)
    
    assert e.value.status_code == 400
    assert e.value.detail == "Score precisa ser positivo"

@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_challenge_already_completed(progress_mock, challenge_mock):
    """Erro: Desafio já cumprido pelo usuario"""
    session = Mock()
    current_user = Mock()

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 1000
    progress.completed = True

    challenge = Mock()
    challenge.id = 1
    challenge.goal = 2000
    challenge.xp_reward = 100
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=1)

    data = UpdateProgressSchema(
        challenge_id = 1,
        score = 200
    )

    progress_mock.return_value = progress
    challenge_mock.return_value = challenge

    with pytest.raises(HTTPException) as e:
        update_progress(data, session, current_user)
    
    assert e.value.status_code == 400
    assert e.value.detail == "Usuario já completou o desafio"