from unittest.mock import Mock
from app.services.challenge_progression_service import reward_all_participants_competition, first_participant_completed

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