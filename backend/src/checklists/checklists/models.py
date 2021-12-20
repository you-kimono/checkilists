from sqlalchemy import Column, Integer, String, ForeignKey

from database.core import Base


class Checklist(Base):
    __tablename__ = 'checklists'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=False, index=True)
    description = Column(String, unique=False, index=False)
    owner_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
