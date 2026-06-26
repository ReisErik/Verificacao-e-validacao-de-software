from fastapi import APIRouter, Depends
from app.schemas.challenge_schema import ChallengeResponseSchema, CreateChallengeSchema
from app.services.challenge_service import create_challenge, get_challenge_or_404, get_all_challenge
from app.core.auth import get_current_user
from app.database.connection import get_session
from sqlmodel import Session

router = APIRouter(
    prefix="/challenge",
    tags=["challenge"]
)

@router.post("/create", response_model=ChallengeResponseSchema, status_code=200)
async def create_challenge_route(data: CreateChallengeSchema, session = Depends(get_session), current_user = Depends(get_current_user)):
    return create_challenge(data, session, current_user)

@router.get("/all", status_code=200)
async def get_all_challenge_route(session = Depends(get_session), current_user = Depends(get_current_user)):
    return get_all_challenge(session, current_user)

@router.get("/{id}", response_model=ChallengeResponseSchema, status_code=200)
async def get_challenge_route(id: int, session = Depends(get_session), current_user = Depends(get_current_user)):
    return get_challenge_or_404(id, session, current_user)

