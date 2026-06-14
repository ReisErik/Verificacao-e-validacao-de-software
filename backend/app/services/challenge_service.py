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

def create_challenge(data: CreateChallengeSchema ,session,current_user):
    validateAuth(current_user)

    if data.end_date <= data.start_date:
        raise HTTPException(
            status_code=400,
            detail="Data final deve ser maior que a inicial."
        )

    challenge = Challenge(
        owner = current_user.id,
        name = data.name,
        description = data.description,
        xp_reward = data.xp_reward,
        type_challenge = data.type_challenge,
        goal = data.goal,
        visibility = data.visibility,
        start_date = data.start_date,
        end_date = data.end_date,
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
 
      

