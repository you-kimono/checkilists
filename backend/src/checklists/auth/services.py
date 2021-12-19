from sqlalchemy.orm import Session

from . import crud, models, exceptions, token
from .hashing import Hash


async def register(profile: models.Profile, db: Session):
    return await crud.save_profile(profile, db)


async def login(email: str, password: str, db: Session):
    profile = await crud.get_profile_by_email(email, db)
    if not profile or not Hash.verify(profile.password, password):
        raise exceptions.LoginFailed()
    access_token_expires = token.timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": profile.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def delete_profile_by_id(profile_id: int, db: Session):
    return await crud.delete_profile(profile_id, db)


async def get_profile_by_id(profile_id: int, db: Session):
    return await crud.get_profile_by_id(profile_id, db)
