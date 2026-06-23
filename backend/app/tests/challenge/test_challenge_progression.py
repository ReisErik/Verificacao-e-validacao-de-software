import pytest
from unittest.mock import Mock, patch
from app.validators.validate_auth import validateAuth
from app.services.challenge_progression_service import get_progress_or_404, update_progress, reward_all_participants
from app.models.challenge_progress import ChallengeProgress
from app.schemas.challenge_schema import ProgressResponseSchema, ChallengeResponseSchema, UpdateProgressSchema, ChallengeType,ChallengeMode
from fastapi import HTTPException
from datetime import datetime, UTC, timedelta, date

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

@patch("app.services.challenge_progression_service.get_total_score_today")
@patch("app.services.challenge_progression_service.create_log")
@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_time_success(progress_mock, challenge_mock, update_streak_mock, create_log_mock, total_score_mock):
    """Sucesso: Atualizou progresso do desafio, finalizou e adicionou XP"""
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 12
    progress.completed = False
    progress.xp_granted = False

    challenge = Mock()
    challenge.id = 1
    challenge.xp_reward = 100
    challenge.goal = 14
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=5)
    challenge.type_challenge = ChallengeType.TIME
    challenge.mode_challenge = ChallengeMode.SOLO

    data = UpdateProgressSchema(
        challenge_id=1,
        score=2
    )

    create_log_mock.return_value = 1
    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge
    total_score_mock.return_value = 0

    response = update_progress(data, session, current_user)

    session.commit.assert_called_once()
    session.refresh.assert_called_with(progress)

    assert response.current_progress == 14
    assert response.completed is True

    assert current_user.xp == 100

    session.add.assert_any_call(progress)
    session.add.assert_any_call(current_user)

@patch("app.services.challenge_progression_service.get_total_score_today")
@patch("app.services.challenge_progression_service.create_log")
@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_time_partial_progress(progress_mock, challenge_mock,update_streak_mock, create_log_mock, total_score_mock):
    """Sucesso: Atualizou progresso do desafio mas não completou"""
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 0
    progress.completed = False

    challenge = Mock()
    challenge.id = 1
    challenge.goal = 14
    challenge.xp_reward = 100
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=5)
    challenge.type_challenge = ChallengeType.TIME

    data = UpdateProgressSchema(
        challenge_id=1,
        score=2
    )

    create_log_mock.return_value = 1
    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge
    total_score_mock.return_value = 0

    response = update_progress(data, session, current_user)

    assert progress.current_progress == 2
    assert progress.completed is False
    assert response.current_progress == 2
    assert response.completed is False
    assert current_user.xp == 0

    session.commit.assert_called_once()

@patch("app.services.challenge_progression_service.get_total_score_today")
@patch("app.services.challenge_progression_service.create_log")
@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_amount_success(progress_mock, challenge_mock, update_streak_mock, create_log_mock, total_score_mock):
    """Sucesso: Atualizou progresso do desafio, finalizou e adicionou XP"""
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 65
    progress.completed = False
    progress.xp_granted = False

    challenge = Mock()
    challenge.id = 1
    challenge.xp_reward = 100
    challenge.goal = 70
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=5)
    challenge.type_challenge = ChallengeType.AMOUNT
    challenge.mode_challenge = ChallengeMode.SOLO

    data = UpdateProgressSchema(
        challenge_id=1,
        score=5
    )

    create_log_mock.return_value = 1
    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge
    total_score_mock.return_value = 0

    response = update_progress(data, session, current_user)

    session.commit.assert_called_once()
    session.refresh.assert_called_with(progress)

    assert response.current_progress == 70
    assert response.completed is True

    assert current_user.xp == 100

    session.add.assert_any_call(progress)
    session.add.assert_any_call(current_user)

@patch("app.services.challenge_progression_service.reward_all_participants")
@patch("app.services.challenge_progression_service.all_participants_completed")
@patch("app.services.challenge_progression_service.get_total_score_today")
@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.create_log")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_group_rewards_all(progress_mock, challenge_mock, update_streak_mock, create_log_mock, total_score_mock, all_completed_mock, reward_all_mock):
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.current_progress = 9
    progress.completed = False
    progress.xp_granted = False

    challenge = Mock()
    challenge.id = 1
    challenge.goal = 10
    challenge.xp_reward = 100
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=1)
    challenge.type_challenge = ChallengeType.AMOUNT
    challenge.mode_challenge = ChallengeMode.GROUP

    create_log_mock.return_value = 1
    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge
    total_score_mock.return_value = 0
    all_completed_mock.return_value = True

    data = UpdateProgressSchema(
        challenge_id=1,
        score=1,
    )

    update_progress(data, session, current_user)

    all_completed_mock.assert_called_once_with(challenge, session)
    reward_all_mock.assert_called_once_with(challenge, session)

@patch("app.services.challenge_progression_service.reward_all_participants_competition")
@patch("app.services.challenge_progression_service.first_participant_completed")
@patch("app.services.challenge_progression_service.get_total_score_today")
@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.create_log")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_competition_rewards_all(progress_mock, challenge_mock, update_streak_mock, create_log_mock, total_score_mock, first_completed_mock, reward_competition_mock):
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.current_progress = 9
    progress.completed = False
    progress.xp_granted = False

    challenge = Mock()
    challenge.id = 1
    challenge.goal = 10
    challenge.xp_reward = 100
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=1)
    challenge.type_challenge = ChallengeType.AMOUNT
    challenge.mode_challenge = ChallengeMode.COMPETITION

    create_log_mock.return_value = 1
    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge
    total_score_mock.return_value = 0
    first_completed_mock.return_value = True

    data = UpdateProgressSchema(
        challenge_id=1,
        score=1,
    )

    update_progress(data, session, current_user)

    first_completed_mock.assert_called_once_with(challenge, session)
    reward_competition_mock.assert_called_once_with(challenge, session)

@patch("app.services.challenge_progression_service.reward_all_participants")
@patch("app.services.challenge_progression_service.all_participants_completed")
@patch("app.services.challenge_progression_service.create_log")
@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.get_total_score_today")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_group_not_all_completed(progress_mock, challenge_mock, update_streak_mock, create_log_mock, total_score_mock, all_completed_mock, reward_all_mock):
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.current_progress = 9
    progress.completed = False
    progress.xp_granted = False

    challenge = Mock()
    challenge.id = 1
    challenge.goal = 10
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=1)
    challenge.type_challenge = ChallengeType.AMOUNT
    challenge.mode_challenge = ChallengeMode.GROUP

    create_log_mock.return_value = 1
    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge
    total_score_mock.return_value = 0
    all_completed_mock.return_value = False

    data = UpdateProgressSchema(
        challenge_id=1,
        score=1,
    )

    update_progress(data, session, current_user)

    all_completed_mock.assert_called_once_with(challenge, session)
    reward_all_mock.assert_not_called()

@patch("app.services.challenge_progression_service.reward_all_participants_competition")
@patch("app.services.challenge_progression_service.first_participant_completed")
@patch("app.services.challenge_progression_service.create_log")
@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.get_total_score_today")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_competition_no_first_completed(progress_mock, challenge_mock, update_streak_mock, create_log_mock, total_score_mock, first_completed_mock, reward_competition_mock):
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.current_progress = 9
    progress.completed = False
    progress.xp_granted = False

    challenge = Mock()
    challenge.id = 1
    challenge.goal = 10
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=1)
    challenge.type_challenge = ChallengeType.AMOUNT
    challenge.mode_challenge = ChallengeMode.COMPETITION

    create_log_mock.return_value = 1
    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge
    total_score_mock.return_value = 0
    first_completed_mock.return_value = False

    data = UpdateProgressSchema(
        challenge_id=1,
        score=1,
    )

    update_progress(data, session, current_user)

    first_completed_mock.assert_called_once_with(challenge, session)
    reward_competition_mock.assert_not_called()

@patch("app.services.challenge_progression_service.get_total_score_today")
@patch("app.services.challenge_progression_service.create_log")
@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_amount_partial_progress(progress_mock, challenge_mock,update_streak_mock, create_log_mock, total_score_mock):
    """Sucesso: Atualizou progresso do desafio mas não completou"""
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 0
    progress.completed = False

    challenge = Mock()
    challenge.id = 1
    challenge.goal = 70
    challenge.xp_reward = 100
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=5)
    challenge.type_challenge = ChallengeType.AMOUNT

    data = UpdateProgressSchema(
        challenge_id=1,
        score=10
    )

    create_log_mock.return_value = 1
    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge
    total_score_mock.return_value = 0

    response = update_progress(data, session, current_user)

    assert progress.current_progress == 10
    assert progress.completed is False
    assert response.current_progress == 10
    assert response.completed is False
    assert current_user.xp == 0

    session.commit.assert_called_once()

@patch("app.services.challenge_progression_service.get_total_score_today")
@patch("app.services.challenge_progression_service.create_log")
@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_amount_score_exceed_limit(progress_mock, challenge_mock,update_streak_mock, create_log_mock, total_score_mock):
    """Sucesso: Atualizou progresso do desafio mas não completou"""
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 0
    progress.completed = False

    challenge = Mock()
    challenge.id = 1
    challenge.goal = 120
    challenge.xp_reward = 120
    challenge.start_date = datetime.now(UTC)
    challenge.end_date = challenge.start_date + timedelta(days=5)
    challenge.type_challenge = ChallengeType.AMOUNT

    create_log_mock.return_value = 1
    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge
    total_score_mock.return_value = 0

    data = UpdateProgressSchema(
        challenge_id=1,
        score=41
    )

    with pytest.raises(HTTPException) as e:
        update_progress(data,session,current_user)

    assert e.value.status_code == 400
    assert e.value.detail == "Pontuação inserida ultrapassa o limite diário" 

@patch("app.services.challenge_progression_service.get_total_score_today")
@patch("app.services.challenge_progression_service.create_log")
@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_amount_score_exceed_limit_daily(progress_mock, challenge_mock,update_streak_mock, create_log_mock, total_score_mock):
    """Sucesso: Atualizou progresso do desafio mas não completou"""
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 0
    progress.completed = False

    challenge = Mock()
    challenge.id = 1
    challenge.goal = 120
    challenge.xp_reward = 120
    challenge.start_date = datetime.now(UTC)
    challenge.end_date = challenge.start_date + timedelta(days=5)
    challenge.type_challenge = ChallengeType.AMOUNT

    create_log_mock.return_value = 1
    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge
    total_score_mock.return_value = 40

    data = UpdateProgressSchema(
        challenge_id=1,
        score=1
    )

    with pytest.raises(HTTPException) as e:
        update_progress(data,session,current_user)

    assert e.value.status_code == 400
    assert e.value.detail == "Pontuação inserida ultrapassa o limite diário" 

@patch("app.services.challenge_progression_service.get_total_score_today")
@patch("app.services.challenge_progression_service.create_log")
@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_time_score_exceed_limit(progress_mock, challenge_mock,update_streak_mock, create_log_mock, total_score_mock):
    """Sucesso: Atualizou progresso do desafio mas não completou"""
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 0
    progress.completed = False

    challenge = Mock()
    challenge.id = 1
    challenge.goal = 18
    challenge.xp_reward = 120
    challenge.start_date = datetime.now(UTC)
    challenge.end_date = challenge.start_date + timedelta(days=5)
    challenge.type_challenge = ChallengeType.TIME

    create_log_mock.return_value = 1
    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge
    total_score_mock.return_value = 0

    data = UpdateProgressSchema(
        challenge_id=1,
        score=4.6
    )

    with pytest.raises(HTTPException) as e:
        update_progress(data,session,current_user)

    assert e.value.status_code == 400
    assert e.value.detail == "Pontuação inserida ultrapassa o limite diário" 

@patch("app.services.challenge_progression_service.get_total_score_today")
@patch("app.services.challenge_progression_service.create_log")
@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_time_score_exceed_limit_daily(progress_mock, challenge_mock,update_streak_mock, create_log_mock, total_score_mock):
    """Sucesso: Atualizou progresso do desafio mas não completou"""
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 0
    progress.completed = False

    challenge = Mock()
    challenge.id = 1
    challenge.goal = 18
    challenge.xp_reward = 120
    challenge.start_date = datetime.now(UTC)
    challenge.end_date = challenge.start_date + timedelta(days=5)
    challenge.type_challenge = ChallengeType.TIME

    create_log_mock.return_value = 1
    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge
    total_score_mock.return_value = 4.5

    data = UpdateProgressSchema(
        challenge_id=1,
        score=0.1
    )

    with pytest.raises(HTTPException) as e:
        update_progress(data,session,current_user)

    assert e.value.status_code == 400
    assert e.value.detail == "Pontuação inserida ultrapassa o limite diário" 

@patch("app.services.challenge_progression_service.create_log")
@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_streak_success(progress_mock, challenge_mock, update_streak_mock, create_log_mock):
    """Sucesso: Atualizou progresso do desafio de Streak, finalizou e adicionou XP"""
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 1
    progress.completed = False
    progress.last_update = (datetime.now(UTC) - timedelta(days=1)).date()
    progress.xp_granted = False
    progress.last_update = date.today() - timedelta(days=1)

    challenge = Mock()
    challenge.id = 1
    challenge.xp_reward = 100
    challenge.goal = 2
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=1)
    challenge.type_challenge = ChallengeType.STREAK
    challenge.mode_challenge = ChallengeMode.SOLO

    data = UpdateProgressSchema(
        challenge_id=1,
        score=1
    )

    create_log_mock.return_value = 1
    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge

    response = update_progress(data, session, current_user)

    session.commit.assert_called_once()
    session.refresh.assert_called_with(progress)

    assert response.current_progress == 2
    assert response.completed is True

    assert current_user.xp == 100

    session.add.assert_any_call(progress)
    session.add.assert_any_call(current_user)

@patch("app.services.challenge_progression_service.create_log")
@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_streak_partial_progress(progress_mock, challenge_mock, update_streak_mock, create_log_mock):
    """Sucesso: Atualizou progresso do desafio Streak, finalizou e adicionou progresso"""
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 1
    progress.completed = False
    progress.last_update = (datetime.now(UTC) - timedelta(days=1)).date()

    challenge = Mock()
    challenge.id = 1
    challenge.xp_reward = 100
    challenge.goal = 3
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=1)
    challenge.type_challenge = ChallengeType.STREAK

    data = UpdateProgressSchema(
        challenge_id=1,
        score=1
    )

    create_log_mock.return_value = 1
    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge

    response = update_progress(data, session, current_user)

    session.commit.assert_called_once()
    session.refresh.assert_called_with(progress)

    assert progress.current_progress == 2
    assert progress.completed is False
    assert response.current_progress == 2
    assert response.completed is False
    assert current_user.xp == 0

@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_streak_partial_progress(progress_mock, challenge_mock, update_streak_mock):
    """Sucesso: Atualizou progresso do desafio Streak, finalizou e adicionou progresso"""
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 1
    progress.completed = False
    progress.last_update = datetime.now(UTC).date()

    challenge = Mock()
    challenge.id = 1
    challenge.xp_reward = 100
    challenge.goal = 3
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=1)
    challenge.type_challenge = ChallengeType.STREAK

    data = UpdateProgressSchema(
        challenge_id=1,
        score=1
    )

    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge

    with pytest.raises(HTTPException) as e:
        update_progress(data, session, current_user)

    assert e.value.status_code == 400
    assert e.value.detail == "Você já registrou progresso hoje."

@patch("app.services.challenge_progression_service.create_log")
@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_streak_last_update_more_1_day(progress_mock, challenge_mock, update_streak_mock, create_log_mock):
    """Sucesso: Atualizou progresso do desafio de Streak, finalizou e adicionou XP"""
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 1
    progress.completed = False
    progress.last_update = (datetime.now(UTC) - timedelta(days=1)).date()
    progress.xp_granted = False
    progress.last_update = date.today() - timedelta(days=2)

    challenge = Mock()
    challenge.id = 1
    challenge.xp_reward = 100
    challenge.goal = 2
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=1)
    challenge.type_challenge = ChallengeType.STREAK
    challenge.mode_challenge = ChallengeMode.SOLO

    data = UpdateProgressSchema(
        challenge_id=1,
        score=1
    )

    create_log_mock.return_value = 1
    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge

    response = update_progress(data, session, current_user)

    session.commit.assert_called_once()
    session.refresh.assert_called_with(progress)

    assert response.current_progress == 1

    session.add.assert_any_call(progress)


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
    assert e.value.detail == "Usuário já completou o desafio"

@patch("app.services.challenge_progression_service.get_total_score_today")
@patch("app.services.challenge_progression_service.create_log")
@patch("app.services.challenge_progression_service.update_streak")
@patch("app.services.challenge_progression_service.get_challenge_or_404")
@patch("app.services.challenge_progression_service.get_progress_or_404")
def test_update_progress_xp_not_received_two_times(progress_mock, challenge_mock, update_streak_mock, create_log_mock, total_score_mock):
    """Sucesso: Atualizou progresso do desafio, finalizou e adicionou XP"""
    session = Mock()

    current_user = Mock()
    current_user.xp = 0

    progress = Mock()
    progress.challenge_id = 1
    progress.current_progress = 65
    progress.completed = False
    progress.xp_granted = True

    challenge = Mock()
    challenge.id = 1
    challenge.xp_reward = 100
    challenge.goal = 70
    challenge.start_date = datetime.now(UTC) - timedelta(days=1)
    challenge.end_date = datetime.now(UTC) + timedelta(days=5)
    challenge.type_challenge = ChallengeType.AMOUNT
    challenge.mode_challenge = ChallengeMode.SOLO

    data = UpdateProgressSchema(
        challenge_id=1,
        score=5
    )

    create_log_mock.return_value = 1
    update_streak_mock.return_value = 1
    progress_mock.return_value = progress
    challenge_mock.return_value = challenge
    total_score_mock.return_value = 0

    response = update_progress(data, session, current_user)

    session.commit.assert_called_once()
    session.refresh.assert_called_with(progress)

    assert response.current_progress == 70
    assert current_user.xp == 0

