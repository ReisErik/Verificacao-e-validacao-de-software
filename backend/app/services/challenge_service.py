from fastapi import HTTPException
from app.models.challenge import Challenge
from app.models.challenge_progress import ChallengeProgress
from app.models.challenge_invite import ChallengeInvite
from app.models.challenge_participant import ChallengeParticipant
from app.validators.validate_auth import validateAuth
from app.services.user_services import get_user_or_404
from sqlmodel import select
from datetime import datetime, UTC
from app.schemas.challenge_schema import CreateChallengeSchema, JoinChallengeSchema
from app.services.calculate_xp import calculate_xp
from app.schemas.challenge_schema import ChallengeType
from app.utils.calculate_duration_days import calculate_duration_days
  
def validate_goal(goal, duration_days, challenge_type):
    effort_per_day = goal / duration_days

    if challenge_type == ChallengeType.STREAK:
        if goal > duration_days:
            raise HTTPException(
                status_code=400,
                detail="Desafios STREAK não podem ter meta maior que a duração."
            )

        elif goal > 30:
            raise HTTPException(
                status_code=400,
                detail="Desafios STREAK podem ter no máximo 30 dias."
            )
        elif goal < 3:
            raise HTTPException(
                status_code=400,
                detail="Desafios Streak precisam ter no mínimo 3 dias"
            )

    elif challenge_type == ChallengeType.TIME:
        if effort_per_day > 3:
            raise HTTPException(
                status_code=400,
                detail="Desafios TIME não podem exigir mais de 3 horas por dia."
            )
        elif effort_per_day < 0.25:
            raise HTTPException(
                status_code=400,
                detail="Desafios TIME precisam ter pelo menos 15 minutos por dia."
            )

    elif challenge_type == ChallengeType.AMOUNT:
        if effort_per_day > 20:
            raise HTTPException(
                status_code=400,
                detail="Desafios AMOUNT não podem exigir mais de 20 unidades por dia."
            )
        elif effort_per_day < 1:
            raise HTTPException(
                status_code=400,
                detail="Desafios AMOUNT precisam ter pelo menos 1 unidade por dia."
            )

def create_challenge(data: CreateChallengeSchema ,session, current_user):
    validateAuth(current_user)

    if data.end_date <= data.start_date:
        raise HTTPException(
            status_code=400,
            detail="Data final deve ser maior que a inicial."
        )

    duration_days = calculate_duration_days(data.start_date, data.end_date)

    validate_goal(
        goal=data.goal,
        duration_days=duration_days,
        challenge_type=data.type_challenge,
    )

    xp_reward = calculate_xp(
        goal=data.goal,
        start_date=data.start_date,
        end_date=data.end_date,
        challenge_type=data.type_challenge,
        category=data.category,
        )

    challenge = Challenge(
        owner = current_user.id,
        name = data.name,
        description = data.description,
        xp_reward = xp_reward,
        type_challenge = data.type_challenge,
        goal = data.goal,
        visibility = data.visibility,
        start_date = data.start_date,
        end_date = data.end_date,
        category = data.category,
        mode_challenge = data.mode_challenge
    )

    session.add(challenge)
    session.flush()

    challenge_progress = ChallengeProgress(
        challenge_id = challenge.id,
        user_id = current_user.id,
        current_progress = 0,
        completed = False,
    )
    
    challenge_participant = ChallengeParticipant(
        user_id = current_user.id,
        challenge_id = challenge.id
    )

    session.add(challenge_participant)
    session.add(challenge_progress)
    session.commit()
    session.refresh(challenge)

    return challenge

def get_challenge_or_404(challenge_id:int , session, current_user):
    validateAuth(current_user)

    challenge = session.get(Challenge, challenge_id)
    if not challenge:
        raise HTTPException(
            status_code=404,
            detail="Desafio não encontrado"
        )
    return challenge

def get_all_challenge(session, current_user):
    validateAuth(current_user)

    challenges = session.exec(
        select(Challenge).where(
            Challenge.visibility.is_(True)
        )
    ).all()

    return challenges
 
      

