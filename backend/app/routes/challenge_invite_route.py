from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.connection import get_session
from app.core.auth import get_current_user

from app.services.challenge_invite_service import (
    invite_challenge,
    cancel_invite,
    get_invite_or_404,
    get_all_invites_sends,
    get_all_invites_receives,
)

router = APIRouter(
    prefix="/challenge/invite",
    tags=["challenge_invite"]
)

@router.post("/send/{challenge_id}/{user_invitated_id}", status_code=200)
async def invite_challenge_route(
    challenge_id: int,
    user_invitated_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return invite_challenge(
        challenge_id,
        user_invitated_id,
        session,
        current_user,
    )

@router.get("/get/{invite_id}", status_code=200)
async def get_invite_route(
    invite_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return get_invite_or_404(
        invite_id,
        session,
        current_user,
    )

@router.delete("/cancel/{invite_id}/{user_invitated_id}", status_code=200)
async def cancel_invite_route(
    invite_id: int,
    user_invitated_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return cancel_invite(
        invite_id,
        user_invitated_id,
        session,
        current_user,
    )

@router.get("/sent", status_code=200)
async def get_all_invites_sent_route(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return get_all_invites_sends(
        session,
        current_user,
    )

@router.get("/received", status_code=200)
async def get_all_invites_received_route(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return get_all_invites_receives(
        session,
        current_user,
    )