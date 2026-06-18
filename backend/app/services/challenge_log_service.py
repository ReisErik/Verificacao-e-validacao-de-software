from app.models.challenge_log import ChallengeLog
from fastapi import HTTPException
from app.schemas.challenge_schema import ChallengeLogSchema

def create_log(challenge_id:int, user_id: int, score:float, session):
    log = ChallengeLogSchema(
        challenge_id=challenge_id,
        user_id=user_id,
        score=score,
    )
    session.add(log)

