from database.core import Base
from sqlalchemy import Column, Integer, String


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, unique=False, index=False)
