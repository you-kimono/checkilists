from sqlalchemy import Column, Integer, String

from database.core import Base


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, unique=False, index=False)
