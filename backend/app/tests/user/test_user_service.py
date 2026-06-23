from unittest.mock import Mock, patch
import pytest
from fastapi import HTTPException
from app.services.user_services import create_user, get_user_or_404, update_user_password,update_streak
from app.schemas.user_schema import UserCreateSchema
from datetime import datetime, date, timedelta,UTC

def test_create_user():
    session = Mock()
    data = UserCreateSchema(
    first_name= "joao",
    last_name= "pedro",
    unique_name= "joaopedro1",
    email= "joao@email.com",
    password= "teste123!",
    role= "user",
    )

    session.exec.return_value.first.return_value = None

    response = create_user(data, session)
    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()

    assert response.first_name == data.first_name

def test_create_user_same_email():
    session = Mock()
    data = UserCreateSchema(
    first_name= "joao",
    last_name= "pedro",
    unique_name= "joaopedro1",
    email= "joao@email.com",
    password= "teste123!",
    role= "user",
    )

    user_same_email = Mock()

    session.exec.return_value.first.side_effect = [
        user_same_email,
        None
    ]

    with pytest.raises(HTTPException) as e:
        create_user(data, session)

    session.add.assert_not_called()
    session.commit.assert_not_called()
    session.refresh.assert_not_called()

    assert e.value.status_code == 400
    assert e.value.detail == "Email já cadastrado."

def test_create_user_same_unique_name():
    session = Mock()
    data = UserCreateSchema(
    first_name= "joao",
    last_name= "pedro",
    unique_name= "joaopedro1",
    email= "joao@email.com",
    password= "teste123!",
    role= "user",
    )

    user_same_unique_name = Mock()

    session.exec.return_value.first.side_effect = [
        None,
        user_same_unique_name
    ]

    with pytest.raises(HTTPException) as e:
        create_user(data, session)

    session.add.assert_not_called()
    session.commit.assert_not_called()
    session.refresh.assert_not_called()

    assert e.value.status_code == 400
    assert e.value.detail == "Unique name já cadastrado."

def test_get_user():
    session = Mock()
    user = Mock()
    session.get.return_value = user

    response = get_user_or_404(1,session)
    session.get.assert_called_once()

    assert response == user

def test_get_user_not_find():
    session = Mock()
    session.get.return_value = None

    with pytest.raises(HTTPException) as e:
        get_user_or_404(1, session)
    
    session.get.assert_called_once()

    assert e.value.status_code == 404
    assert e.value.detail == "Usuário não encontrado."


@patch("app.services.user_services.get_user_or_404")
@patch("app.services.user_services.hash_password")
@patch("app.services.user_services.verify_password")
def test_update_user_password(mock_verify_password, mock_hash_password, mock_get_user):
    session = Mock()
    User = Mock()
    User.password = "teste123!"

    mock_get_user.return_value = User
    mock_hash_password.return_value = "abc123"
    mock_verify_password.return_value = False

    response = update_user_password(1,"teste123!",session)
    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert response == User

@patch("app.services.user_services.get_user_or_404")
@patch("app.services.user_services.hash_password")
@patch("app.services.user_services.verify_password")
def test_update_user_same_password(mock_verify_password, mock_hash_password, mock_get_user):
    session = Mock()
    User = Mock()
    User.password = "teste123!"

    mock_get_user.return_value = User
    mock_hash_password.return_value = "teste123!"
    mock_verify_password.return_value = True

    with pytest.raises(HTTPException) as e:
        update_user_password(1,"teste123!",session)
    
    assert e.value.status_code == 400
    assert e.value.detail == "Nova senha deve ser diferente da senha atual."

def test_update_streak():
    session = Mock()
    current_user = Mock()
    current_user.last_workout = datetime.now(UTC) - timedelta(days=1)
    current_user.streak = 0
    current_user.best_streak = 2

    update_streak(current_user, datetime.now(UTC), session)

    assert current_user.streak == 1
    assert current_user.best_streak == 2

def test_update_streak_and_best():
    session = Mock()
    current_user = Mock()
    current_user.last_workout = datetime.now(UTC) - timedelta(days=1)
    current_user.streak = 2
    current_user.best_streak = 2

    update_streak(current_user, datetime.now(UTC), session)

    assert current_user.streak == 3
    assert current_user.best_streak == 3