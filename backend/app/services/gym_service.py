from fastapi import HTTPException
from app.models.gym import Gym
from app.services.user_services import get_user
from app.validators.validate_gym import validate_gym
from app.validators.validate_auth import validateAuth
from sqlmodel import select

def get_gym(gym_id, session):
    gym = session.get(Gym, gym_id)
    if not gym:
        raise HTTPException(status_code=404, detail="Academia não encontrada.")
    return gym

def get_all_gyms(session):
    gyms = session.exec(
        select(Gym)
    ).all()

    return gyms

def create_gym(data, session, current_user):
    validateAuth(current_user)
    
    validate_gym(data.name, data.location, current_user.id)

    gym = Gym(
        name=data.name,
        location=data.location,
        owner_id=current_user.id
    )

    session.add(gym)
    session.commit()
    session.refresh(gym)

    return gym

def delete_gym(gym_id, session, current_user):
    validateAuth(current_user)

    gym = get_gym(gym_id, session)
    
    if current_user.id != gym.owner_id  :
        raise HTTPException(status_code=403, detail="Apenas o dono pode deletar a academia.")

    session.delete(gym)
    session.commit()

def update_gym(gym_id, data, session, current_user):
    validateAuth(current_user)

    gym = get_gym(gym_id, session)

    if current_user.id != gym.owner_id  :
        raise HTTPException(status_code=403, detail="Apenas o dono pode atualizar a academia.")

    validate_gym(data.name, data.location, gym.owner_id)

    gym.name = data.name
    gym.location = data.location

    session.add(gym)
    session.commit()
    session.refresh(gym)

    return gym

def update_owner_gym(gym_id, new_owner_id, session, current_user):
    validateAuth(current_user)

    gym = get_gym(gym_id, session)

    if current_user.id != gym.owner_id  :
        raise HTTPException(status_code=403, detail="Apenas o dono pode atualizar a academia.")

    new_owner = get_user(new_owner_id, session)

    if new_owner.id == gym.owner_id:
        raise HTTPException(status_code=400, detail="O novo dono deve ser diferente do atual.")

    gym.owner_id = new_owner.id

    session.add(gym)
    session.commit()
    session.refresh(gym)

    return gym