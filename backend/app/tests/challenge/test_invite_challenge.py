from app.services.challenge_invite_service import invite_exists, invite_challenge, get_invite_or_404, cancel_invite
from unittest.mock import Mock, patch
from fastapi import HTTPException
import pytest

def test_invite_not_exists():
    session = Mock()
    current_user = Mock()
    invite = None

    session.exec.return_value.first.return_value = invite
    assert invite_exists(1, 1, session, current_user) is None 

def test_invite_exist():
    session = Mock()
    current_user = Mock()
    invite = Mock()

    session.exec.return_value.first.return_value = invite 


    with pytest.raises(HTTPException) as e:
        invite_exists(1, 1, session, current_user)   
    assert e.value.status_code == 400
    assert e.value.detail == "Convite já enviado"

def test_get_invite_or_404_found():
    session = Mock()
    current_user = Mock()

    invite = Mock()
    invite.id = 1

    session.get.return_value = invite

    result = get_invite_or_404(1, session, current_user)

    assert result.id == 1

def test_get_invite_or_404_not_found():
    session = Mock()
    current_user = Mock()

    session.get.return_value = None

    with pytest.raises(HTTPException) as e:
        get_invite_or_404(1, session, current_user)

    assert e.value.status_code == 404

@patch("app.services.challenge_invite_service.invite_exists")
@patch("app.services.challenge_invite_service.get_challenge_or_404")
@patch("app.services.challenge_invite_service.get_user_or_404")
def test_invite_challenge_success(mock_get_user, mock_get_challenge, mock_invite_exists):
    """Caminho feliz: Dono convida um usuário válido que ainda não foi convidado"""
    session = Mock()
    current_user = Mock()
    current_user.id = 1  

    challenge_mock = Mock()
    challenge_mock.owner = 1  
    mock_get_challenge.return_value = challenge_mock
    
    result = invite_challenge(challenge_id=10, user_invitated_id=2, session=session, current_user=current_user)

    mock_invite_exists.assert_called_once_with(10, 2, session, current_user)
    mock_get_challenge.assert_called_once_with(10, session, current_user)
    mock_get_user.assert_called_once_with(2, session)
    
    session.add.assert_called_once()
    session.commit.assert_called_once()
    
    assert result.sender_id == 1
    assert result.receiver_id == 2
    assert result.challenge_id == 10
    assert result.sent is True


@patch("app.services.challenge_invite_service.invite_exists")
@patch("app.services.challenge_invite_service.get_challenge_or_404")
@patch("app.services.challenge_invite_service.get_user_or_404")
def test_invite_challenge_owner_inviting_himself(mock_get_user, mock_get_challenge, mock_invite_exists):
    """Erro: Dono tenta convidar a si mesmo"""
    session = Mock()
    current_user = Mock()
    current_user.id = 1

    with pytest.raises(HTTPException) as e:
        invite_challenge(10, 1, session, current_user)

    assert e.value.status_code == 403
    assert e.value.detail == "Dono não pode convidar a si mesmo"
    session.commit.assert_not_called()


@patch("app.services.challenge_invite_service.invite_exists")
@patch("app.services.challenge_invite_service.get_challenge_or_404")
@patch("app.services.challenge_invite_service.get_user_or_404")
def test_invite_challenge_not_owner(mock_get_user, mock_get_challenge, mock_invite_exists):
    """Erro: Usuário que não é o dono tenta convidar alguém"""
    session = Mock()
    current_user = Mock()
    current_user.id = 2  

    challenge_mock = Mock()
    challenge_mock.owner = 1

    mock_get_challenge.return_value = challenge_mock

    with pytest.raises(HTTPException) as e:
        invite_challenge(10, 3, session, current_user)

    assert e.value.status_code == 403
    assert e.value.detail == "Apenas o dono pode convidar"
    session.commit.assert_not_called()

@patch("app.services.challenge_invite_service.get_user_or_404")
@patch("app.services.challenge_invite_service.get_invite_or_404")
def test_cancel_invite_success(mock_get_invite, mock_get_user):
    session = Mock()
    current_user = Mock()
    current_user.id = 1

    invite = Mock()
    invite.sender_id = 1
    invite.sent = True
    invite.answer = None
    invite.id = 1

    mock_get_invite.return_value = invite
    session.delete.return_value = None

    response = cancel_invite(1, 1, session, current_user)

    session.delete.assert_called_with(invite)
    session.commit.assert_called_once()
    assert response == {"message": "Convite cancelado"}    

@patch("app.services.challenge_invite_service.get_user_or_404")
@patch("app.services.challenge_invite_service.get_invite_or_404")
def test_cancel_invite_sender_not_user(mock_get_invite, mock_get_user):
    session = Mock()
    current_user = Mock()
    current_user.id = 1
    
    invite = Mock()
    invite.id = 2
    invite.sent = True
    invite.answer = True

    mock_get_invite.return_value = invite

    with pytest.raises(HTTPException) as e:
        cancel_invite(1, 1, session, current_user)

    assert e.value.status_code == 400
    assert e.value.detail == "Usuario não é dono do convite"

@patch("app.services.challenge_invite_service.get_user_or_404")
@patch("app.services.challenge_invite_service.get_invite_or_404")
def test_cancel_invite_not_sent(mock_get_invite, mock_get_user):
    session = Mock()
    current_user = Mock()
    current_user.id = 1

    invite = Mock()
    invite.sender_id = 1
    invite.id = 1
    invite.sent = False

    mock_get_invite.return_value = invite

    with pytest.raises(HTTPException) as e:
        cancel_invite(1, 1, session, current_user)

    assert e.value.status_code == 400
    assert e.value.detail == "Convite não foi enviado"

@patch("app.services.challenge_invite_service.get_user_or_404")
@patch("app.services.challenge_invite_service.get_invite_or_404")
def test_cancel_invite_already_answer(mock_get_invite, mock_get_user):
    session = Mock()
    current_user = Mock()
    current_user.id = 1

    invite = Mock()
    invite.sender_id = 1
    invite.id = 1
    invite.sent = True
    invite.answer = True

    mock_get_invite.return_value = invite

    with pytest.raises(HTTPException) as e:
        cancel_invite(1, 1, session, current_user)

    assert e.value.status_code == 400
    assert e.value.detail == "Convite já foi aceito"