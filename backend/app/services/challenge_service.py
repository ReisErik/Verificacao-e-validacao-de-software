from fastapi import HTTPException
from app.models.challenge import Challenge
from app.models.challenge_progress import ChallengeProgress
from app.models.challenge_invite import ChallengeInvite
from app.models.challenge_participant import ChallengeParticipant
from app.validators.validate_auth import validateAuth
from app.services.user_services import get_user_or_404
from sqlmodel import select
from datetime import datetime

from enum import Enum

class ChallengeType(Enum):
    STREAK = "Streak"
    TIME = "Time"

def create_challenge(data,session,current_user):
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
 
      
def invite_exists(challenge_id: int, user_invitated_id: int, session, current_user):
    validateAuth(current_user)

    invite = session.exec(
        select(ChallengeInvite).where(
            ChallengeInvite.challenge_id == challenge_id,
            ChallengeInvite.receiver_id == user_invitated_id
            )
    ).first()

    if invite:
        raise HTTPException(
            status_code=400,
            detail="Convite já enviado"
        )
    
    
def invite_challenge(challenge_id: int, user_invitated_id: int, session, current_user):
    validateAuth(current_user)

    invite_exists(challenge_id, user_invitated_id ,session, current_user)
    challenge = get_challenge_or_404(challenge_id, session, current_user)
    get_user_or_404(user_invitated_id, session)

    if user_invitated_id == current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Dono não pode convidar a si mesmo"
        )

    if current_user.id != challenge.owner:
        raise HTTPException(
            status_code=403,
            detail="Apenas o dono pode convidar"
        )
    
    invite = ChallengeInvite(
        sender_id=current_user.id,
        receiver_id=user_invitated_id,
        challenge_id=challenge_id,
        sent=True
    )

    session.add(invite)
    session.commit()
    session.refresh(invite)

    return invite

def get_invite_or_404(invite_id: int, session, current_user):
    validateAuth(current_user)
    invite = session.get(ChallengeInvite, invite_id)
    if not invite:
        raise HTTPException(
            status_code=404,
            detail="Desafio não encontrado"
        )
    return invite

def ensure_not_participant(participant_id:int, challenge_id: int, session, current_user):
    validateAuth(current_user)
    
    participant = session.exec(
        select(ChallengeParticipant).where(
            ChallengeParticipant.user_id == participant_id,
            ChallengeParticipant.challenge_id == challenge_id
            )
    ).first()

    if participant:
        raise HTTPException(
            status_code=400,
            detail="Usuario já está participando do desafio"
        )


def join_or_refuse_challenge(data, session, current_user):
    validateAuth(current_user)

    answer = data.answer
    challenge = get_challenge_or_404(data.challenge_id, session, current_user)
    invite = get_invite_or_404(data.invite_id, session, current_user)
    ensure_not_participant(current_user.id, challenge.id, session, current_user)

    if invite.receiver_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Convite não pertence ao usuario"
        )
    
    if invite.answer is not None:
        raise HTTPException(
            status_code=400,
            detail="Convite já respondido"
        )
    
    if challenge.end_date < datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Desafio encerrado"
        )
    
    if challenge.start_date < datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Desafio já começou"
        )
    
    if not answer:
        invite.answer = False
    else:
        invite.answer = True
        challenge_progress = ChallengeProgress(
            challenge_id = invite.challenge_id,
            user_id = current_user.id,
            current_progress = 0,
            completed = False,
        )

        challenge_participant = ChallengeParticipant(
            user_id = current_user.id,
            challenge_id = invite.challenge_id 
        )
        session.add(challenge_progress)
        session.add(challenge_participant)

    session.add(invite)
    session.commit()
    session.refresh(invite)

    return invite
