from app.validators.validate_auth import validateAuth
from sqlmodel import select
from app.models.challenge_participant import ChallengeParticipant
from fastapi import HTTPException
from app.services.challenge_service import get_challenge_or_404
from app.services.challenge_invite_service import get_invite_or_404
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