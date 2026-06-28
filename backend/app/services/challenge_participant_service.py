from app.validators.validate_auth import validateAuth
from sqlmodel import select
from app.models.challenge_participant import ChallengeParticipant
from fastapi import HTTPException
from app.services.challenge_service import get_challenge_or_404
from app.services.challenge_invite_service import get_invite_or_404, ensure_challenge_has_slot
from app.services.challenge_progression_service import get_progress_or_404
from app.services.challenge_service import ensure_active_challenge_limit
from app.models.challenge_progress import ChallengeProgress
from datetime import datetime, UTC, date
from app.schemas.challenge_schema import JoinChallengeSchema
from app.utils.ensure_utc import ensure_utc
from app.models.challenge import Challenge

def ensure_not_participant(participant_id:int, challenge_id: int, session, current_user):
    """ Verificar se o usuario já esta participando do desafio"""
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

def ensure_participants_limit(challenge, session):
    """ Verificar se o desafio ja está com vaga disponivel"""
    participants = session.exec(
    select(ChallengeParticipant).where(
        ChallengeParticipant.challenge_id == challenge.id
        )
    ).all()

    if len(participants) >= challenge.max_participants:
        raise HTTPException(
            status_code=400,
            detail="Desafio atingiu o limite de participantes",
        )

def join_or_refuse_challenge(data: JoinChallengeSchema , session, current_user):
    """
    Aceitar ou recusar convite para usuario
    Aceitar caso: Usuario não participe; Usuario não atingiu limite de desafios em andamento; Desafio possui vagas disponiveis
                  Foi aceito dentro de 7 dias, Apenas o usuario que recebeu pode aceitar, Convite não foi respondido

    """
    validateAuth(current_user)

    answer = data.answer
    challenge = get_challenge_or_404(data.challenge_id, session, current_user)
    invite = get_invite_or_404(data.invite_id, session, current_user)

    ensure_not_participant(current_user.id, challenge.id, session, current_user)
    ensure_active_challenge_limit(current_user, session)
    ensure_participants_limit(challenge, session)

    if (date.today() - invite.created_at).days > 7:
        invite.answer = False
        session.add(invite)
        session.commit()
        raise HTTPException(
            status_code=403,
            detail="Convite expirado"
        )

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
    
    if ensure_utc(challenge.end_date) < datetime.now(UTC):
        raise HTTPException(
            status_code=400,
            detail="Desafio encerrado"
        )
    
    remaining_days = (challenge.end_date.date() - date.today()).days + 1
    total_days = (challenge.end_date.date() - challenge.start_date.date()).days + 1
    
    if remaining_days < total_days / 2:
        raise HTTPException(
            status_code=400,
            detail="O período para ingresso neste desafio já foi encerrado."
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
    """ Buscar registro de participação do usuario """
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
    """Buscar todos os desafios que o usuário participa"""
    validateAuth(current_user)

    challenges = session.exec(
        select(Challenge)
        .join(ChallengeParticipant, Challenge.id == ChallengeParticipant.challenge_id)
        .where(ChallengeParticipant.user_id == current_user.id)
    ).all()

    return challenges

def get_latest_user_challenge_or_none(challenge_id: int, session, current_user):
    """ Buscar o usuario mais antigo do desafio após o dono"""
    user = session.exec(
        select(ChallengeParticipant).where(
            ChallengeParticipant.challenge_id == challenge_id,
            ChallengeParticipant.user_id != current_user.id
        ).order_by(ChallengeParticipant.created_at)
    ).first()

    return user

def leave_challenge(challenge_id: int, session, current_user):
    """
    Sair do desafio
    Aceito caso: desafio, participação e progressão existir, desafio ainda não foi encerrado ou completo pelo usuario
    Caso o dono sair, usuario mais antigo registrado assume o cargo de dono do desafio
    """
    validateAuth(current_user)

    challenge = get_challenge_or_404(challenge_id, session, current_user)
    challenge_participate = get_challenge_participate(challenge_id, session, current_user)
    challenge_progression = get_progress_or_404(challenge_id, session, current_user)
    new_owner = get_latest_user_challenge_or_none(challenge_id,session,current_user)

    if ensure_utc(challenge.end_date) < datetime.now(UTC):
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
    ):
        challenge.owner = new_owner.user_id
        session.add(challenge)
        
    elif challenge.owner == current_user.id:
        session.delete(challenge)

    session.delete(challenge_participate)
    session.delete(challenge_progression)

    session.commit()

    return {
        "message": "Usuario saiu do desafio"
    }





    

