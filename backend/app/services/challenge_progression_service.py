from app.models.challenge_progress import ChallengeProgress
from app.validators.validate_auth import validateAuth
from app.services.challenge_service import get_challenge_or_404
from app.services.challenge_participant_service import ensure_not_participant
from sqlmodel import select
from fastapi import HTTPException

def get_progress_or_404(challenge_id: int, session, current_user):
    validateAuth(current_user)

    progress = session.exec(
        select(ChallengeProgress).where(
            ChallengeProgress.challenge_id == challenge_id,
            ChallengeProgress.user_id == current_user.id
        )
    ).first()

    if not progress:
        raise HTTPException(
            status_code = 404,
            detail = "Usuario não está participando deste desafio"
        )




