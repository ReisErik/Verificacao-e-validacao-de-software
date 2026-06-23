from unittest.mock import Mock
from app.services.challenge_progression_service import all_participants_completed, reward_all_participants

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