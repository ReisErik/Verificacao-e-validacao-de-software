from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.connection import get_session
from app.core.auth import get_current_user

from app.schemas.challenge_schema import UpdateProgressSchema, ProgressResponseSchema

from app.services.challenge_progression_service import (
    get_progress_or_404,
    update_progress,
)

router = APIRouter(
    prefix="/challenge/progress",
    tags=["challenge_progress"]
)


@router.get(
    "/get/{challenge_id}",
    response_model=ProgressResponseSchema,
    status_code=200,
)
async def get_progress_route(
    challenge_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return get_progress_or_404(
        challenge_id,
        session,
        current_user,
    )


@router.patch(
    "/update",
    response_model=ProgressResponseSchema,
    status_code=200,
)
async def update_progress_route(
    data: UpdateProgressSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return update_progress(
        data,
        session,
        current_user,
    )