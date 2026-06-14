from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.connection import get_session
from app.core.auth import get_current_user
from app.schemas.challenge_schema import JoinChallengeSchema

from app.services.challenge_participant_service import (
    join_or_refuse_challenge,
    get_challenge_participate,
    get_all_challenge_participate,
    leave_challenge,
)

router = APIRouter(
    prefix="/challenge/participant",
    tags=["challenge_participant"]
)

@router.post("/join", status_code=200)
async def join_or_refuse_challenge_route(
    data: JoinChallengeSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return join_or_refuse_challenge(
        data,
        session,
        current_user,
    )

@router.get("/get/all", status_code=200)
async def get_all_challenge_participate_route(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return get_all_challenge_participate(
        session,
        current_user,
    )

@router.get("/get/{challenge_id}", status_code=200)
async def get_challenge_participate_route(
    challenge_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return get_challenge_participate(
        challenge_id,
        session,
        current_user,
    )

@router.delete("/leave/{challenge_id}", status_code=200)
async def leave_challenge_route(
    challenge_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return leave_challenge(
        challenge_id,
        session,
        current_user,
    )