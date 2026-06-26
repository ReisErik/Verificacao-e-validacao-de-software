from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserCreateSchema, UserResponseSchema, UserUpdatePasswordSchema
from app.services.user_services import create_user, get_user_or_404, update_user_password, delete_user, disable_user, get_all_user_public
from app.database.connection import get_session
from sqlmodel import Session
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/user", response_model=UserResponseSchema, status_code=200)
async def create_user_route(data: UserCreateSchema, session: Session = Depends(get_session)):
    return create_user(data, session)

@router.get("/user/all", status_code=200)
async def get_all_users_route(current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    return get_all_user_public(current_user, session)

@router.put("/user/{id}/password", response_model=UserResponseSchema, status_code=200)
async def update_password_route(id: int, data: UserUpdatePasswordSchema, session: Session = Depends(get_session)):
    return update_user_password(id, data.new_password, session)

@router.delete("/user/{id}/delete", status_code=204)
async def delete_user_route(id: int, session: Session = Depends(get_session)):
    delete_user(id, session)
    return

@router.post("/user/{id}/disable", response_model=UserResponseSchema, status_code=200)
async def disable_user_route(id: int, session: Session = Depends(get_session)):
    return disable_user(id, session)
