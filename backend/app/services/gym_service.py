from fastapi import HTTPException
from app.models.gym import Gym
from app.validators.validate_gym import validate_gym


def create_gym(data, session):
    validate_gym(data.name, data.location, data.owner_id)

    gym = Gym(
        name=data.name,
        location=data.location,
        owner_id=data.owner_id
    )

    session.add(gym)
    session.commit()
    session.refresh(gym)

    return gym