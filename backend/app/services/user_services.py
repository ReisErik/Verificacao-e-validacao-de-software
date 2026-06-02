from fastapi import HTTPException
from app.models.user import User
from app.core.security import hash_password, verify_password
from sqlmodel import select
from app.validators.validate_user import validate_name, validate_unique_name, validate_password

def create_user(data, session):
    password = data.password
    validate_password(password)
    validate_name(data.first_name, data.last_name)

    lower_unique_name = data.unique_name.lower()
    validate_unique_name(lower_unique_name)

    hashed_password = hash_password(password)

    user_same_email = session.exec(
        select(User).where(User.email == data.email)
    ).first()

    user_same_unique_name = session.exec(
        select(User).where(User.unique_name == lower_unique_name)
    ).first()

    if user_same_email:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado."
        )
    if user_same_unique_name:
        raise HTTPException(
            status_code=400,
            detail="Unique name já cadastrado."
        )
    
    user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        unique_name=lower_unique_name,
        email=data.email,
        password=hashed_password,
        role=data.role,
        active=True
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user(id: int, session):
    user = session.get(User, id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )
    return user

def update_user_password(id:int, new_password: str, session):
    validate_password(new_password)
    user = get_user(id, session)
    
    if verify_password(new_password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Nova senha deve ser diferente da senha atual."
        )
    
    user.password = hash_password(new_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete_user(id: int, session):
    user = get_user(id, session)
    
    session.delete(user)
    session.commit()
    return {"message": "Usuário deletado."}

def disable_user(id: int, session):
    user = get_user(id, session)
    
    user.active = False
    session.add(user)
    session.commit()
    session.refresh(user)
    return user