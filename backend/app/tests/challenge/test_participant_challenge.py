from app.services.challenge_participant_service import ensure_not_participant, join_or_refuse_challenge, get_challenge_participate, get_all_challenge_participate,leave_challenge
from unittest.mock import Mock, patch
from fastapi import HTTPException
import pytest
from datetime import datetime, UTC, timedelta, date
from app.utils.constantes import *

def test_ensure_not_participant():
    """Correto: Verifica se usuario não está participando do desafio"""
    session = Mock()
    current_user = Mock()
    participant = None

    session.exec.return_value.first.return_value = participant
    assert ensure_not_participant(1, 1, session, current_user) is None

def test_ensure_participant():
    """Erro: Verifica se usuario já esta participando do desafio"""
    session = Mock()
    current_user = Mock()
    participant = Mock()

    session.exec.return_value.first.return_value = participant
    
    with pytest.raises(HTTPException) as e:
        ensure_not_participant(1, 1, session, current_user)   
    
    assert e.value.status_code == 400
    assert e.value.detail == "Usuario já está participando do desafio"

@patch("app.services.challenge_participant_service.ensure_not_participant")
@patch("app.services.challenge_participant_service.get_invite_or_404")
@patch("app.services.challenge_participant_service.get_challenge_or_404")
def test_join_challenge_accept_success(mock_get_challenge, mock_get_invite, mock_ensure_not_participant):
    """Correto: Usuário aceita o convite válido de um desafio ativo"""
    session = Mock()
    session.exec.return_value.all.return_value = []

    current_user = Mock()
    current_user.id = 2  

    data = Mock()
    data.challenge_id = 10
    data.invite_id = 5
    data.answer = True

    challenge_mock = Mock()
    challenge_mock.id = 10
    challenge_mock.end_date = datetime.now(UTC) + timedelta(days=5)
    challenge_mock.max_participants = 5

    mock_get_challenge.return_value = challenge_mock

    invite_mock = Mock()
    invite_mock.challenge_id = 10
    invite_mock.receiver_id = 2  
    invite_mock.answer = None    
    invite_mock.created_at = date.today()

    mock_get_invite.return_value = invite_mock

    result = join_or_refuse_challenge(data, session, current_user)

    assert invite_mock.answer is True
    assert session.add.call_count == 3  
    session.commit.assert_called_once()
    assert result == invite_mock


@patch("app.services.challenge_participant_service.ensure_not_participant")
@patch("app.services.challenge_participant_service.get_invite_or_404")
@patch("app.services.challenge_participant_service.get_challenge_or_404")
def test_join_challenge_expired(mock_get_challenge, mock_get_invite, mock_ensure_not_participant):
    """Erro: Usuário tenta aceitar convite de desafio que já acabou"""
    session = Mock()
    session.exec.return_value.all.return_value = []

    current_user = Mock()
    current_user.id = 2

    data = Mock()
    data.challenge_id = 10
    data.invite_id = 5
    data.answer = True

    challenge_mock = Mock()
    challenge_mock.end_date = datetime.now(UTC) - timedelta(days=2)
    challenge_mock.max_participants = 5

    mock_get_challenge.return_value = challenge_mock

    invite_mock = Mock()
    invite_mock.receiver_id = 2
    invite_mock.answer = None
    invite_mock.created_at = date.today()

    mock_get_invite.return_value = invite_mock

    with pytest.raises(HTTPException) as e:
        join_or_refuse_challenge(data, session, current_user)

    assert e.value.status_code == 400
    assert e.value.detail == "Desafio encerrado"
    session.commit.assert_not_called()

@patch("app.services.challenge_participant_service.ensure_not_participant")
@patch("app.services.challenge_participant_service.get_invite_or_404")
@patch("app.services.challenge_participant_service.get_challenge_or_404")
def test_join_challenge_invite_wrong_user(mock_get_challenge, mock_get_invite, mock_ensure_not_participant):
    """Erro: Usuário tenta aceitar convite de outro usuario"""
    session = Mock()
    session.exec.return_value.all.return_value = []

    current_user = Mock()
    current_user.id = 2

    data = Mock()
    data.challenge_id = 10
    data.invite_id = 5
    data.answer = True

    challenge_mock = Mock()
    challenge_mock.end_date = datetime.now(UTC) + timedelta(days=2)
    challenge_mock.max_participants = 5

    mock_get_challenge.return_value = challenge_mock

    invite_mock = Mock()
    invite_mock.receiver_id = 3
    invite_mock.answer = None
    invite_mock.created_at = date.today()
    
    mock_get_invite.return_value = invite_mock

    with pytest.raises(HTTPException) as e:
        join_or_refuse_challenge(data, session, current_user)

    assert e.value.status_code == 403
    assert e.value.detail == "Convite não pertence ao usuario"
    session.commit.assert_not_called()

@patch("app.services.challenge_participant_service.ensure_not_participant")
@patch("app.services.challenge_participant_service.get_invite_or_404")
@patch("app.services.challenge_participant_service.get_challenge_or_404")
def test_join_challenge_refuse_success(mock_get_challenge,mock_get_invite,mock_ensure_not_participant):
    """Correto: Usuario recusa o convite do desafio"""
    session = Mock()
    session.exec.return_value.all.return_value = []

    current_user = Mock()
    current_user.id = 2

    data = Mock()
    data.challenge_id = 10
    data.invite_id = 5
    data.answer = False

    challenge_mock = Mock()
    challenge_mock.id = 10
    challenge_mock.end_date = datetime.now(UTC) + timedelta(days=2)
    challenge_mock.max_participants = 5

    mock_get_challenge.return_value = challenge_mock

    invite_mock = Mock()
    invite_mock.receiver_id = 2
    invite_mock.answer = None
    invite_mock.created_at = date.today()

    mock_get_invite.return_value = invite_mock

    result = join_or_refuse_challenge(data, session, current_user)

    assert result.answer is False
    session.commit.assert_called_once()
    assert session.add.call_count == 1
    
@patch("app.services.challenge_participant_service.ensure_not_participant")
@patch("app.services.challenge_participant_service.get_invite_or_404")
@patch("app.services.challenge_participant_service.get_challenge_or_404")
def test_join_challenge_already_answered_true(mock_get_challenge, mock_get_invite, mock_ensure_not_participant):
    """Erro: Usuário tenta aceitar convite de desafio que já foi aceito"""
    session = Mock()
    session.exec.return_value.all.return_value = []

    current_user = Mock()
    current_user.id = 2

    data = Mock()
    data.challenge_id = 10
    data.invite_id = 5
    data.answer = True

    challenge_mock = Mock()
    challenge_mock.end_date = datetime.now(UTC) + timedelta(days=2)
    challenge_mock.max_participants = 5

    mock_get_challenge.return_value = challenge_mock

    invite_mock = Mock()
    invite_mock.receiver_id = 2
    invite_mock.answer = True
    invite_mock.created_at = date.today()

    mock_get_invite.return_value = invite_mock

    with pytest.raises(HTTPException) as e:
        join_or_refuse_challenge(data, session, current_user)

    assert e.value.status_code == 400
    assert e.value.detail == "Convite já respondido"
    session.commit.assert_not_called()

@patch("app.services.challenge_participant_service.ensure_not_participant")
@patch("app.services.challenge_participant_service.get_invite_or_404")
@patch("app.services.challenge_participant_service.get_challenge_or_404")
def test_join_challenge_already_answered_false(mock_get_challenge, mock_get_invite, mock_ensure_not_participant):
    """Erro: Usuário tenta aceitar convite de desafio que ja foi recusado"""
    session = Mock()
    session.exec.return_value.all.return_value = []

    current_user = Mock()
    current_user.id = 2

    data = Mock()
    data.challenge_id = 10
    data.invite_id = 5
    data.answer = True

    challenge_mock = Mock()
    challenge_mock.end_date = datetime.now(UTC) + timedelta(days=2)
    challenge_mock.max_participants = 5

    mock_get_challenge.return_value = challenge_mock

    invite_mock = Mock()
    invite_mock.receiver_id = 2
    invite_mock.answer = False
    invite_mock.created_at = date.today()

    mock_get_invite.return_value = invite_mock

    with pytest.raises(HTTPException) as e:
        join_or_refuse_challenge(data, session, current_user)

    assert e.value.status_code == 400
    assert e.value.detail == "Convite já respondido"
    session.commit.assert_not_called()

@patch("app.services.challenge_participant_service.ensure_not_participant")
@patch("app.services.challenge_participant_service.get_invite_or_404")
@patch("app.services.challenge_participant_service.get_challenge_or_404")
def test_join_challenge_invite_expired(mock_get_challenge, mock_get_invite, mock_ensure_not_participant):
    """Erro: Usuário tenta aceitar convite de desafio que ja foi recusado"""
    session = Mock()
    session.exec.return_value.all.return_value = []

    current_user = Mock()
    current_user.id = 2

    data = Mock()
    data.challenge_id = 10
    data.invite_id = 5
    data.answer = True

    challenge_mock = Mock()
    challenge_mock.end_date = datetime.now(UTC) + timedelta(days=2)
    challenge_mock.max_participants = 5

    mock_get_challenge.return_value = challenge_mock

    invite_mock = Mock()
    invite_mock.receiver_id = 2
    invite_mock.answer = False
    invite_mock.created_at = date.today() - timedelta(days=8)

    mock_get_invite.return_value = invite_mock

    with pytest.raises(HTTPException) as e:
        join_or_refuse_challenge(data, session, current_user)

    assert e.value.status_code == 403
    assert e.value.detail == "Convite expirado"

@patch("app.services.challenge_participant_service.ensure_not_participant")
@patch("app.services.challenge_participant_service.get_invite_or_404")
@patch("app.services.challenge_participant_service.get_challenge_or_404")
def test_join_challenge_but_limit_exceed(mock_get_challenge, mock_get_invite, mock_ensure_not_participant):
    """Erro: Usuário tenta aceitar convite de desafio, mas já esta com o máximo de desafios"""
    session = Mock()

    current_user = Mock()
    current_user.id = 2

    data = Mock()
    data.challenge_id = 10
    data.invite_id = 5
    data.answer = True

    session.exec.return_value.all.return_value = ["A" for _ in range(MAX_ACTIVE_CHALLENGES)]

    challenge_mock = Mock()
    challenge_mock.end_date = datetime.now(UTC) + timedelta(days=2)

    mock_get_challenge.return_value = challenge_mock

    invite_mock = Mock()
    invite_mock.receiver_id = 2
    invite_mock.answer = False
    invite_mock.created_at = date.today() - timedelta(days=8)

    mock_get_invite.return_value = invite_mock

    with pytest.raises(HTTPException) as e:
        join_or_refuse_challenge(data, session, current_user)

    assert e.value.status_code == 400
    assert e.value.detail == "Limite de desafios ativos atingido"

def test_get_challenge_participate_success():
    session = Mock()
    current_user = Mock()
    current_user.id = 1

    challenge = Mock()
    challenge.id = 1

    session.exec.return_value.first.return_value = challenge

    result = get_challenge_participate(1 ,session, current_user)

    assert result == challenge

def test_get_challenge_participate_empty():
    session = Mock()
    current_user = Mock()
    current_user.id = 1

    session.exec.return_value.first.return_value = None

    with pytest.raises(HTTPException) as e:
        get_challenge_participate(1,session, current_user)

    assert e.value.status_code == 404
    assert e.value.detail == "Usuario não participa deste desafio"

def test_get_all_challenges_success():
    session = Mock()
    current_user = Mock()
    current_user.id = 1

    challenges = [Mock(), Mock()]

    exec_mock = Mock()
    exec_mock.all.return_value = challenges

    session.exec.return_value = exec_mock

    result = get_all_challenge_participate(session, current_user)

    assert result == challenges

def test_get_all_challenges_empty():
    session = Mock()
    current_user = Mock()
    current_user.id = 1

    session.exec.return_value.all.return_value = []

    assert get_all_challenge_participate(session, current_user) == []

@patch("app.services.challenge_participant_service.get_latest_user_challenge_or_none")
@patch("app.services.challenge_participant_service.get_progress_or_404")
@patch("app.services.challenge_participant_service.get_challenge_participate")
@patch("app.services.challenge_participant_service.get_challenge_or_404")
def test_leave_challenge_and_delete_success(challenge_mock, challenge_participate_mock, progress_mock, latest_user_mock):

    session = Mock()
    current_user = Mock()
    current_user.id = 1

    challenge = Mock()
    challenge.id = 1
    challenge.owner = 1
    challenge.end_date = datetime.now(UTC) + timedelta(days=1)

    progress = Mock()
    progress.completed = False

    participate = Mock()

    challenge_mock.return_value = challenge
    challenge_participate_mock.return_value = participate 
    progress_mock.return_value = progress
    latest_user_mock.return_value = None

    assert leave_challenge(1,session, current_user) == {
        "message": "Usuario saiu do desafio"
    }
    assert session.delete.call_count == 3
    session.commit.assert_called_once()

@patch("app.services.challenge_participant_service.get_latest_user_challenge_or_none")
@patch("app.services.challenge_participant_service.get_progress_or_404")
@patch("app.services.challenge_participant_service.get_challenge_participate")
@patch("app.services.challenge_participant_service.get_challenge_or_404")
def test_leave_challenge_and_replacement_new_owner_success(challenge_mock, challenge_participate_mock, progress_mock, latest_user_mock):

    session = Mock()
    current_user = Mock()
    current_user.id = 1

    challenge = Mock()
    challenge.id = 1
    challenge.owner = 1
    challenge.end_date = datetime.now(UTC) + timedelta(days=1)

    progress = Mock()
    progress.completed = False

    owner = Mock()
    owner.user_id = 2

    participate = Mock()

    challenge_mock.return_value = challenge
    challenge_participate_mock.return_value = participate
    progress_mock.return_value = progress
    latest_user_mock.return_value = owner

    assert leave_challenge(1,session, current_user) == {
        "message": "Usuario saiu do desafio"
    }
    session.add.assert_called_once()
    assert session.delete.call_count == 2
    session.commit.assert_called_once()

@patch("app.services.challenge_participant_service.get_latest_user_challenge_or_none")
@patch("app.services.challenge_participant_service.get_progress_or_404")
@patch("app.services.challenge_participant_service.get_challenge_participate")
@patch("app.services.challenge_participant_service.get_challenge_or_404")
def test_leave_challenge_challenge_already_finished(challenge_mock, challenge_participate_mock, progress_mock, latest_user_mock):

    session = Mock()
    current_user = Mock()
    current_user.id = 1

    challenge = Mock()
    challenge.id = 1
    challenge.owner = 1
    challenge.end_date = datetime.now(UTC) - timedelta(days=1)

    challenge_mock.return_value = challenge

    with pytest.raises(HTTPException) as e:
        leave_challenge(1,session, current_user) 

    assert e.value.status_code == 400
    assert e.value.detail == "Desafio já foi encerrado"

@patch("app.services.challenge_participant_service.get_latest_user_challenge_or_none")
@patch("app.services.challenge_participant_service.get_progress_or_404")
@patch("app.services.challenge_participant_service.get_challenge_participate")
@patch("app.services.challenge_participant_service.get_challenge_or_404")
def test_leave_challenge_challenge_already_completed(challenge_mock, challenge_participate_mock, progress_mock, latest_user_mock):

    session = Mock()
    current_user = Mock()
    current_user.id = 1

    challenge = Mock()
    challenge.id = 1
    challenge.owner = 1
    challenge.end_date = datetime.now(UTC) + timedelta(days=1)

    challenge_progression = Mock()
    challenge_progression.completed = True

    challenge_mock.return_value = challenge
    progress_mock.return_value = challenge_progression

    with pytest.raises(HTTPException) as e:
        leave_challenge(1,session, current_user) 

    assert e.value.status_code == 400
    assert e.value.detail == "Usuario já finalizou o desafio"

@patch("app.services.challenge_participant_service.ensure_not_participant")
@patch("app.services.challenge_participant_service.get_invite_or_404")
@patch("app.services.challenge_participant_service.get_challenge_or_404")
def test_accept_invite_challenge_already_full(mock_get_challenge, mock_get_invite, mock_ensure_not_participant):
    session = Mock()
    exec_result1 = Mock()
    exec_result1.all.return_value = []

    exec_result2 = Mock()
    exec_result2.all.return_value = ["a" for _ in range(MAX_PARTICIPANTS)]

    session.exec.side_effect = [
        exec_result1,
        exec_result2,
    ]

    current_user = Mock()
    current_user.id = 1

    data = Mock()
    data.challenge_id = 10
    data.invite_id = 5
    data.answer = True

    challenge_mock = Mock()
    challenge_mock.end_date = datetime.now(UTC) + timedelta(days=2)
    challenge_mock.max_participants = 5

    mock_get_challenge.return_value = challenge_mock

    invite_mock = Mock()
    invite_mock.receiver_id = 3
    invite_mock.answer = None
    invite_mock.created_at = date.today()
    
    mock_get_invite.return_value = invite_mock

    with pytest.raises(HTTPException) as e:
        join_or_refuse_challenge(data, session, current_user)

    assert e.value.status_code == 400
    assert e.value.detail == "Desafio atingiu o limite de participantes"
