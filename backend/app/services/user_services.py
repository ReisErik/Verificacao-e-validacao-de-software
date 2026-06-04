from fastapi import HTTPException
from app.models.user import User
from app.core.security import hash_password, verify_password
from sqlmodel import select
from datetime import datetime, timedelta
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

def get_user_or_404(id: int, session):
    user = session.get(User, id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )
    return user

def update_user_password(id:int, new_password: str, session):
    validate_password(new_password)
    user = get_user_or_404(id, session)
    
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
    user = get_user_or_404(id, session)
    
    session.delete(user)
    session.commit()
    return {"message": "Usuário deletado."}

def disable_user(id: int, session):
    user = get_user_or_404(id, session)
    
    user.active = False
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def calculate_xp(id: int, xp: int, session):
    user = get_user_or_404(id, session)

    user.xp += xp
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def update_streak(id: int, current_date : datetime, session):
    user = get_user_or_404(id, session)

    if current_date is None:
        current_date = datetime.now()
    
    if user.last_workout:
        last_workout_date = user.last_workout.date()
        today = current_date.date()
        yesterday = today - timedelta(days=1)

        if last_workout_date == yesterday:
            user.streak += 1
        elif last_workout_date < yesterday:
            user.streak = 1
    else:
        user.streak = 1

    user.last_workout = current_date
    
    if user.streak > user.best_streak:
        user.best_streak = user.streak

    session.add(user)
    session.commit()
    session.refresh(user)
    return user