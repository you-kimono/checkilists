from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from . import models
from .exceptions import EmailAlreadyTaken, InvalidProfile
from .hashing import Hash


async def save_profile(new_profile: models.Profile, database: Session) -> models.Profile:
    new_profile.password = Hash.bcrypt(new_profile.password)
    try:
        database.add(new_profile)
        database.commit()
        database.refresh(new_profile)
    except IntegrityError as e:
        cause: str = e.args[0]
        if 'UNIQUE constraint failed: profiles.email' in cause:
            raise EmailAlreadyTaken()
    return new_profile


async def get_profile_by_id(profile_id: int, database: Session) -> models.Profile:
    profile = database.query(models.Profile).filter(models.Profile.id == profile_id)
    if not profile.first():
        raise InvalidProfile(profile_id=profile_id)
    return profile.first()


async def get_profile_by_email(profile_email: str, database: Session) -> models.Profile:
    profile = database.query(models.Profile).filter(models.Profile.email == profile_email)
    if not profile.first():
        raise InvalidProfile(email=profile_email)
    return profile.first()


async def delete_profile(profile_id: int, database: Session) -> None:
    profile = database.query(models.Profile).filter(models.Profile.id == profile_id)
    if not profile.first():
        raise InvalidProfile(profile_id)
    profile.delete()
    database.commit()
