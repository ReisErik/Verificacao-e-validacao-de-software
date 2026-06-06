from app.services.challenge_participant_service import ensure_not_participant, join_or_refuse_challenge
from unittest.mock import Mock, patch
from fastapi import HTTPException
import pytest
from datetime import datetime, UTC, timedelta

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
    current_user = Mock()
    current_user.id = 2  

    data = Mock()
    data.challenge_id = 10
    data.invite_id = 5
    data.answer = True

    challenge_mock = Mock()
    challenge_mock.id = 10
    challenge_mock.end_date = datetime.now(UTC) + timedelta(days=5)

    mock_get_challenge.return_value = challenge_mock

    invite_mock = Mock()
    invite_mock.challenge_id = 10
    invite_mock.receiver_id = 2  
    invite_mock.answer = None    

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
    current_user = Mock()
    current_user.id = 2

    data = Mock()
    data.challenge_id = 10
    data.invite_id = 5
    data.answer = True

    challenge_mock = Mock()
    challenge_mock.end_date = datetime.now(UTC) - timedelta(days=2)

    mock_get_challenge.return_value = challenge_mock

    invite_mock = Mock()
    invite_mock.receiver_id = 2
    invite_mock.answer = None

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
    current_user = Mock()
    current_user.id = 2

    data = Mock()
    data.challenge_id = 10
    data.invite_id = 5
    data.answer = True

    challenge_mock = Mock()
    challenge_mock.end_date = datetime.now(UTC) + timedelta(days=2)

    mock_get_challenge.return_value = challenge_mock

    invite_mock = Mock()
    invite_mock.receiver_id = 3
    invite_mock.answer = None
    
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

    current_user = Mock()
    current_user.id = 2

    data = Mock()
    data.challenge_id = 10
    data.invite_id = 5
    data.answer = False

    challenge_mock = Mock()
    challenge_mock.id = 10
    challenge_mock.end_date = datetime.now(UTC) + timedelta(days=2)

    mock_get_challenge.return_value = challenge_mock

    invite_mock = Mock()
    invite_mock.receiver_id = 2
    invite_mock.answer = None

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
    current_user = Mock()
    current_user.id = 2

    data = Mock()
    data.challenge_id = 10
    data.invite_id = 5
    data.answer = True

    challenge_mock = Mock()
    challenge_mock.end_date = datetime.now(UTC) + timedelta(days=2)

    mock_get_challenge.return_value = challenge_mock

    invite_mock = Mock()
    invite_mock.receiver_id = 2
    invite_mock.answer = True

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
    current_user = Mock()
    current_user.id = 2

    data = Mock()
    data.challenge_id = 10
    data.invite_id = 5
    data.answer = True

    challenge_mock = Mock()
    challenge_mock.end_date = datetime.now(UTC) + timedelta(days=2)

    mock_get_challenge.return_value = challenge_mock

    invite_mock = Mock()
    invite_mock.receiver_id = 2
    invite_mock.answer = False

    mock_get_invite.return_value = invite_mock

    with pytest.raises(HTTPException) as e:
        join_or_refuse_challenge(data, session, current_user)

    assert e.value.status_code == 400
    assert e.value.detail == "Convite já respondido"
    session.commit.assert_not_called()

