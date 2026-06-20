import pytest
from unittest.mock import Mock, patch
from app.validators.validate_auth import validateAuth
from app.services.challenge_progression_service import reward_all_participants, reward_all_participants_competition, reward_user, all_participants_completed, first_participant_completed

from app.models.challenge_progress import ChallengeProgress
from app.schemas.challenge_schema import ProgressResponseSchema, ChallengeResponseSchema, UpdateProgressSchema, ChallengeType,ChallengeMode
from fastapi import HTTPException
from datetime import datetime, UTC, timedelta, date

def test_reward_user():
    session = Mock()

    user = Mock()
    user.id = 1
    user.xp = 0

    challenge = Mock()
    challenge.xp_reward = 100

    reward_user(user, challenge, session)

    assert user.xp == 100

def test_reward_all_participants():
    session = Mock()

    user1 = Mock()
    user1.id = 1
    user1.xp = 0

    user2 = Mock()
    user2.id = 2
    user2.xp = 50

    users = [user1, user2]

    progress1 = Mock()
    progress1.user_id = 1
    progress1.xp_granted = False
    progress1.completed = False
    progress1.current_progress = 0

    progress2 = Mock()
    progress2.user_id = 2
    progress2.xp_granted = False
    progress2.completed = False
    progress2.current_progress = 0

    progressions = [progress1, progress2]

    challenge = Mock()
    challenge.id = 10
    challenge.xp_reward = 100
    challenge.goal = 5

    session.exec.return_value.all.side_effect = [
        progressions,  
        users        
    ]

    reward_all_participants(challenge, session)

    assert user1.xp == 100
    assert user2.xp == 150

    assert progress1.xp_granted is True
    assert progress2.xp_granted is True

    session.commit.assert_called_once()

def test_all_participants_completed_true():
    session = Mock()

    exec_result = Mock()
    exec_result.first.return_value = None

    session.exec.return_value = exec_result

    challenge = Mock()
    challenge.id = 1

    result = all_participants_completed(challenge, session)

    assert result is True

def test_all_participants_completed_false():
    session = Mock()

    exec_result = Mock()
    exec_result.first.return_value = Mock()

    session.exec.return_value = exec_result

    challenge = Mock()
    challenge.id = 1

    result = all_participants_completed(challenge, session)

    assert result is False

def test_first_participant_completed_true():
    session = Mock()

    exec_result = Mock()
    exec_result.all.return_value = [Mock()]

    session.exec.return_value = exec_result

    challenge = Mock()
    challenge.id = 1

    assert first_participant_completed(challenge, session) is True

def test_first_participant_completed_false():
    session = Mock()

    exec_result = Mock()
    exec_result.all.return_value = [Mock(), Mock()]

    session.exec.return_value = exec_result

    challenge = Mock()
    challenge.id = 1

    assert first_participant_completed(challenge, session) is False

def test_reward_all_participants():
    session = Mock()

    p1 = Mock(user_id=1, xp_granted=False)
    p2 = Mock(user_id=2, xp_granted=False)

    u1 = Mock(id=1, xp=100)
    u2 = Mock(id=2, xp=50)

    exec1 = Mock()
    exec1.all.return_value = [p1, p2]

    exec2 = Mock()
    exec2.all.return_value = [u1, u2]

    session.exec.side_effect = [exec1, exec2]

    challenge = Mock()
    challenge.id = 1
    challenge.xp_reward = 80

    reward_all_participants(challenge, session)

    assert u1.xp == 180
    assert u2.xp == 130

    assert p1.xp_granted is True
    assert p2.xp_granted is True

    session.commit.assert_called_once()

def test_reward_all_participants_skip_already_rewarded():
    session = Mock()

    p1 = Mock(user_id=1, xp_granted=True)

    u1 = Mock(id=1, xp=100)

    exec1 = Mock()
    exec1.all.return_value = [p1]

    exec2 = Mock()
    exec2.all.return_value = [u1]

    session.exec.side_effect = [exec1, exec2]

    challenge = Mock()
    challenge.id = 1
    challenge.xp_reward = 80

    reward_all_participants(challenge, session)

    assert u1.xp == 100

    session.commit.assert_called_once()

def test_reward_all_participants_competition():
    session = Mock()

    p1 = Mock(user_id=1, current_progress=100, updated_at=1, xp_granted=False)
    p2 = Mock(user_id=2, current_progress=90, updated_at=2, xp_granted=False)
    p3 = Mock(user_id=3, current_progress=90, updated_at=3, xp_granted=False)
    p4 = Mock(user_id=4, current_progress=70, updated_at=4, xp_granted=False)
    p5 = Mock(user_id=5, current_progress=60, updated_at=5, xp_granted=False)
    p6 = Mock(user_id=6, current_progress=50, updated_at=6, xp_granted=False)
    p7 = Mock(user_id=7, current_progress=20, updated_at=7, xp_granted=False)
    p8 = Mock(user_id=8, current_progress=0, updated_at=8, xp_granted=False)

    progressions = [p1, p2, p3, p4, p5, p6, p7, p8]

    users = []

    for i in range(1, 9):
        users.append(Mock(id=i, xp=0))

    exec1 = Mock()
    exec1.all.return_value = progressions

    exec2 = Mock()
    exec2.all.return_value = users

    session.exec.side_effect = [exec1, exec2]

    challenge = Mock()
    challenge.id = 1
    challenge.goal = 100
    challenge.xp_reward = 100

    reward_all_participants_competition(challenge, session)

    xp = {u.id: u.xp for u in users}

    assert xp[1] == 120
    assert xp[2] == 110
    assert xp[3] == 100
    assert xp[4] == 80
    assert xp[5] == 80
    assert xp[6] == 50
    assert xp[7] == 0
    assert xp[8] == 0

    session.commit.assert_called_once()

def test_reward_all_participants_competition_already_rewarded():
    session = Mock()

    p1 = Mock(
        user_id=1,
        current_progress=100,
        updated_at=1,
        xp_granted=True,
    )

    exec1 = Mock()
    exec1.all.return_value = [p1]

    session.exec.side_effect = [exec1]

    challenge = Mock()
    challenge.id = 1

    reward_all_participants_competition(challenge, session)

    session.commit.assert_not_called()