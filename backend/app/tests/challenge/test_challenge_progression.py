import pytest
from unittest.mock import Mock, patch
from app.validators.validate_auth import validateAuth
from app.services.challenge_progression_service import get_progress_or_404
from app.models.challenge_progress import ChallengeProgress
from fastapi import HTTPException

def test_get_progress_success():
    session = Mock()
    current_user = Mock()
    current_user.id = 1
    progress = Mock()

    session.exec.return_value.first.return_value = progress
    result = get_progress_or_404(1, session, current_user)
    session.exec.assert_called_once()

    assert result is progress

def test_get_progress_not_found():
    session = Mock()
    current_user = Mock()
    
    session.exec.return_value.first.return_value = None

    with pytest.raises(HTTPException) as e:
        get_progress_or_404(1, session, current_user)
    
    session.exec.assert_called_once()
    assert e.value.status_code == 404
    assert e.value.detail == "Usuario não está participando deste desafio"