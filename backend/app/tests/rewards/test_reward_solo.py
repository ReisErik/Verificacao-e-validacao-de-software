from unittest.mock import Mock
from app.services.challenge_progression_service import reward_user

def test_reward_user():
    session = Mock()

    user = Mock()
    user.id = 1
    user.xp = 0

    challenge = Mock()
    challenge.xp_reward = 100

    reward_user(user, challenge, session)

    assert user.xp == 100