from fastapi import APIRouter, Depends
from app.schemas.login_schema import LoginSchema
from app.services.auth_service import create_token_user 
from app.database.connection import get_session
from app.core.auth import get_current_user
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login")
async def auth(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    return create_token_user(data, session)

@router.get("/me")
async def get_me(current_user = Depends(get_current_user)):
    return current_user