from app.models.challenge_progress import ChallengeProgress
from app.validators.validate_auth import validateAuth
from app.services.challenge_service import get_challenge_or_404
from app.schemas.challenge_schema import UpdateProgressSchema, ProgressResponseSchema
from app.utils.ensure_utc import ensure_utc
from sqlmodel import select
from fastapi import HTTPException
from datetime import datetime, UTC
from app.schemas.challenge_schema import ChallengeType
from app.services.user_services import update_streak

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
    
    return progress

def update_progress(data: UpdateProgressSchema, session, current_user):
    validateAuth(current_user)

    progress = get_progress_or_404(data.challenge_id, session, current_user)
    challenge = get_challenge_or_404(data.challenge_id, session, current_user)

    now = datetime.now(UTC)
    today = now.date()

    if ensure_utc(challenge.start_date) > now:
        raise HTTPException(
            status_code=400,
            detail="Desafio ainda não começou",
        )

    if now > ensure_utc(challenge.end_date):
        raise HTTPException(
            status_code=400,
            detail="Desafio já acabou",
        )

    if progress.completed:
        raise HTTPException(
            status_code=400,
            detail="Usuário já completou o desafio",
        )

    if challenge.type_challenge == ChallengeType.STREAK:

        if progress.last_update == today:
            raise HTTPException(
                status_code=400,
                detail="Você já registrou progresso hoje.",
            )

        if (progress.last_update is not None and (today - progress.last_update).days > 1):
            progress.current_progress = 1
        else:
            progress.current_progress += 1

        progress.last_update = today

    else:
        score = data.score

        if score <= 0:
            raise HTTPException(
                status_code=400,
                detail="Score precisa ser positivo",
            )

        progress.current_progress += score

    if not progress.completed:
        update_streak(current_user.id, datetime.now(UTC), session)

    if progress.current_progress >= challenge.goal:
        progress.completed = True
        progress.current_progress = challenge.goal

        current_user.xp += challenge.xp_reward
        session.add(current_user)

    session.add(progress)
    session.commit()
    session.refresh(progress)

    return ProgressResponseSchema(
        challenge_id=data.challenge_id,
        current_progress=progress.current_progress,
        completed=progress.completed,
    )







