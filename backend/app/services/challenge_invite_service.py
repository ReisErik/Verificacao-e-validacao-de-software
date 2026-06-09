from sqlmodel import select
from fastapi import HTTPException
from app.services.user_services import get_user_or_404
from app.services.challenge_service import get_challenge_or_404
from app.validators.validate_auth import validateAuth
from app.models.challenge_invite import ChallengeInvite

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

def cancel_invite(invite_id: int, user_invitated_id: int, session, current_user):
    validateAuth(current_user)

    invite = get_invite_or_404(invite_id, session, current_user)
    get_user_or_404(user_invitated_id, session)

    if invite.sender_id != current_user.id:
        raise HTTPException(
            status_code = 400,
            detail="Usuario não é dono do convite"
        )

    if invite.sent == False:
        raise HTTPException(
            status_code = 400,
            detail="Convite não foi enviado"
        )
    
    if invite.answer == True:
        raise HTTPException(
            status_code = 400,
            detail="Convite já foi aceito"
        )

    session.delete(invite)
    session.commit()
    
    return {"message": "Convite cancelado"}
