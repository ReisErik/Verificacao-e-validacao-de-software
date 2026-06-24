from app.models.challenge_log import ChallengeLog
from fastapi import HTTPException
from app.schemas.challenge_schema import ChallengeLogSchema
from sqlmodel import select
from app.validators.validate_auth import validateAuth
from datetime import datetime, date
from sqlalchemy import func

def create_log(challenge_id:int, user_id: int, score:float, session):
    log = ChallengeLog(
        challenge_id=challenge_id,
        user_id=user_id,
        score=score,
    )
    session.add(log)

def get_total_score_today(challenge_id: int, current_user, session):
    validateAuth(current_user)
    today = date.today()

    score = session.exec(
        select(func.sum(ChallengeLog.score)).where(
            ChallengeLog.user_id == current_user.id,
            ChallengeLog.challenge_id == challenge_id,
            func.date(ChallengeLog.created_at) == today,
        )
    ).one()

    return score