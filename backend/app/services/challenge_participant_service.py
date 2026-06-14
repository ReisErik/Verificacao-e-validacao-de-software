from app.validators.validate_auth import validateAuth
from sqlmodel import select
from app.models.challenge_participant import ChallengeParticipant
from fastapi import HTTPException
from app.services.challenge_service import get_challenge_or_404
from app.services.challenge_invite_service import get_invite_or_404
from app.services.challenge_progression_service import get_progress_or_404
from app.models.challenge_progress import ChallengeProgress
from datetime import datetime, UTC
from app.schemas.challenge_schema import JoinChallengeSchema

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

def join_or_refuse_challenge(data: JoinChallengeSchema , session, current_user):
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
    
    if challenge.end_date < datetime.now(UTC):
        raise HTTPException(
            status_code=400,
            detail="Desafio encerrado"
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

def get_challenge_participate(challenge_id: int, session, current_user):
    validateAuth(current_user)

    challenges = session.exec(
        select(ChallengeParticipant).where(
            ChallengeParticipant.user_id == current_user.id,
            ChallengeParticipant.challenge_id == challenge_id
        )
    ).first()

    if not challenges:
        raise HTTPException(
            status_code = 404,
            detail="Usuario não participa deste desafio"
        )

    return challenges

def get_all_challenge_participate(session, current_user):
    validateAuth(current_user)

    challenges = session.exec(
        select(ChallengeParticipant).where(
            ChallengeParticipant.user_id == current_user.id
        )
    ).all()

    if not challenges:
        raise HTTPException(
            status_code = 404,
            detail="Usuario não participa de nenhum desafio"
        )

    return challenges

def get_latest_user_challenge_or_none(challenge_id: int, session, current_user):

    user = session.exec(
        select(ChallengeParticipant).where(
            ChallengeParticipant.challenge_id == challenge_id,
            ChallengeParticipant.user_id != current_user.id
        ).order_by(ChallengeParticipant.created_at)
    ).first()

    return user

def leave_challenge(challenge_id: int, session, current_user):
    validateAuth(current_user)

    challenge = get_challenge_or_404(challenge_id, session, current_user)
    challenge_participate = get_challenge_participate(challenge_id, session, current_user)
    challenge_progression = get_progress_or_404(challenge_id, session, current_user)
    new_owner = get_latest_user_challenge_or_none(challenge_id,session,current_user)

    if challenge.end_date < datetime.now(UTC):
        raise HTTPException(
            status_code=400,
            detail="Desafio já foi encerrado"
        )

    if challenge_progression.completed:
        raise HTTPException(
            status_code=400,
            detail="Usuario já finalizou o desafio"
        )

    if (
        challenge.owner == current_user.id
        and new_owner is not None
        and not challenge_progression.completed
    ):
        challenge.owner = new_owner.user_id
        session.add(challenge)
        session.delete(challenge_participate)
        session.delete(challenge_progression)

    elif challenge.owner == current_user.id:
        session.delete(challenge)

    session.commit()

    return {
        "message": "Usuario saiu do desafio"
    }





    

