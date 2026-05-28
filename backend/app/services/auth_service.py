from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from app.core.security import verify_password, create_access_token
from app.models.user import User
from sqlmodel import select

def create_token_user(data, session):
    user = session.exec(
        select(User).where(User.email == data.username)
    ).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado.")
    
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Email ou senha invalidos.")
    
    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


