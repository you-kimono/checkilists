from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from . import models
from .exceptions import EmailAlreadyTaken
from .hashing import Hash


async def save_profile(new_user: models.User, database: Session) -> models.User:
    new_user.password = Hash.bcrypt(new_user.password)
    try:
        database.add(new_user)
        database.commit()
        database.refresh(new_user)
    except IntegrityError as e:
        cause: str = e.args[0]
        if 'UNIQUE constraint failed: users.email' in cause:
            raise EmailAlreadyTaken()
    return new_user

