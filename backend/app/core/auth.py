from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.database.connection import get_session
from sqlmodel import Session
from app.models.user import User
from app.core.security import secret_key, algorithm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token invalido"
    )

    try :
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
        
    user = session.get(User, int(user_id))

    if not user:
        raise credentials_exception

    return user