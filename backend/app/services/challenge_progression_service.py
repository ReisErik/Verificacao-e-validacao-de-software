from app.models.challenge_progress import ChallengeProgress
from app.validators.validate_auth import validateAuth
from app.services.challenge_service import get_challenge_or_404
from app.schemas.challenge_schema import UpdateProgressSchema, ProgressResponseSchema
from app.utils.ensure_utc import ensure_utc
from sqlmodel import select
from fastapi import HTTPException
from datetime import datetime, UTC
from app.schemas.challenge_schema import ChallengeType, ChallengeMode
from app.services.user_services import update_streak
from app.services.challenge_log_service import create_log, get_total_score_today
from app.models.user import User

def get_progress_or_404(challenge_id: int, session, current_user):
    """ Busca o progresso do usuario """
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

def reward_user(current_user, challenge, session):
    """ Recompensa para desafios SOLO """
    validateAuth(current_user)
    current_user.xp += challenge.xp_reward

    session.add(current_user)

    return current_user

def reward_all_participants(challenge, session):
    """ 
    Recompensa para desafios GROUP 
    Distribui a mesma quantidade de XP para todos participantes
    """
    progressions = session.exec(
        select(ChallengeProgress).where(
            ChallengeProgress.challenge_id == challenge.id
        )
    ).all()

    user_ids = [p.user_id for p in progressions]

    users = session.exec(
        select(User).where(User.id.in_(user_ids))
    ).all()

    progress_map = {
        progress.user_id: progress
        for progress in progressions
    }

    for user in users:
        progress = progress_map[user.id]

        if progress.xp_granted:
            continue

        user.xp += challenge.xp_reward
        progress.xp_granted = True

    session.commit()

def all_participants_completed(challenge, session) -> bool:
    """ Verifica se todos participantes completaram o desafio """
    pending = session.exec(
        select(ChallengeProgress)
        .where(
            ChallengeProgress.challenge_id == challenge.id,
            ChallengeProgress.completed == False,
        )
        .limit(1)
    ).first()

    return pending is None

def first_participant_completed(challenge, session) -> bool:
    """ Verifica se foi o primeiro participante a concluir o desafio """
    completed = session.exec(
        select(ChallengeProgress)
        .where(
            ChallengeProgress.challenge_id == challenge.id,
            ChallengeProgress.completed == True,
        )
    ).all()

    return len(completed) == 1

def reward_all_participants_competition(challenge, session):
    """
    Recompensa para desafios COMPETITION
    Distribui XP conforme colocação do desafio
        1º -> 120%, 2º -> 110%, 3º -> 100%, 4º e 5º -> 80%, demais que completaram pelo menos metade do desafio -> 20%, restante -> 0
    """
    progressions = session.exec(
        select(ChallengeProgress).where(
            ChallengeProgress.challenge_id == challenge.id
        )
    ).all()

    progressions = sorted(
        progressions,
        key = lambda p:(
            -p.current_progress,
            p.updated_at
        )
    )

    if any(p.xp_granted for p in progressions):
        return

    user_ids = [p.user_id for p in progressions]

    users = session.exec(
        select(User).where(User.id.in_(user_ids))
    ).all()

    users_map = {user.id: user for user in users}

    for position, progression in enumerate(progressions, start=1):
        user = users_map.get(progression.user_id)

        if user is None or progression.xp_granted:
            continue

        if position == 1:
            multiplier = 1.20
        elif position == 2:
            multiplier = 1.10
        elif position == 3:
            multiplier = 1.00
        elif position in (4, 5):
            multiplier = 0.80
        else:

            if progression.current_progress == 0:
                multiplier = 0.00
            elif progression.current_progress >= challenge.goal / 2:
                multiplier = 0.50
            else:
                multiplier = 0.00

        gained_xp = int(challenge.xp_reward * multiplier)

        user.xp += gained_xp
        progression.xp_granted = True

    session.commit()

def update_progress(data: UpdateProgressSchema, session, current_user):
    """
    Atualiza progresso do desafio
    Aceito caso: Progresso e desafio existam; enquanto estiver com o desafio ativo; usuario não completou
                 Pontuação precisa ser positiva; 
                 Streak: apenas um registro por dia
                 Média diaria é a meta fracionada igualitáriamente entre os dias
                 TIME: No máximo 150% da média diaria
                 AMOUNT: No máximo 200% da médida diaria
    Caso o progresso do usuário alcance a meta, desafio é finalizado quando: 
                 SOLO -> Automáticamente, 
                 GROUP -> Todos participantes terminaram; 
                 COMPETITION -> Assim que o primeiro participante terminar
    A cada Atualização do desafio é criado um LOG e atualizado a STREAK global do usuário caso seja a primeira atualização do dia
    """
    validateAuth(current_user)

    progress = get_progress_or_404(data.challenge_id, session, current_user)
    challenge = get_challenge_or_404(data.challenge_id, session, current_user)

    now = datetime.now(UTC)
    today = now.date()

    FACTOR_MAX = {
        ChallengeType.TIME: 1.5,
        ChallengeType.AMOUNT: 2.0
    }

    duration_days = max((challenge.end_date - challenge.start_date).days + 1,1)

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

        score_per_day = challenge.goal / duration_days
        score_max_per_day = score_per_day * FACTOR_MAX[challenge.type_challenge]

        score_today = get_total_score_today(data.challenge_id, current_user, session) or 0
        
        if score_today + score > score_max_per_day:
            raise HTTPException(
                status_code=400,
                detail="Pontuação inserida ultrapassa o limite diário"
            )

        progress.last_update = today
        progress.current_progress += score

    if not progress.completed:
        update_streak(current_user, datetime.now(UTC), session)

    if progress.current_progress >= challenge.goal:
        progress.completed = True
        progress.current_progress = challenge.goal

        session.flush()

        if challenge.mode_challenge == ChallengeMode.SOLO and not progress.xp_granted:
            reward_user(current_user, challenge, session)
            progress.xp_granted = True

        elif challenge.mode_challenge == ChallengeMode.GROUP and not progress.xp_granted:
            if all_participants_completed(challenge, session):
                reward_all_participants(challenge, session)
        
        elif challenge.mode_challenge == ChallengeMode.COMPETITION and not progress.xp_granted:
            if first_participant_completed(challenge, session):
                reward_all_participants_competition(challenge, session)

    create_log(
        challenge_id=data.challenge_id,
        user_id=current_user.id,
        score=score if challenge.type_challenge != ChallengeType.STREAK else 1,
        session=session,
    )

    session.add(progress)
    session.commit()
    session.refresh(progress)

    return ProgressResponseSchema(
        challenge_id=data.challenge_id,
        current_progress=progress.current_progress,
        completed=progress.completed,
    )







