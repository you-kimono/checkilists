from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from database.core import Base


class Checklist(Base):
    __tablename__ = 'checklists'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=False, index=True)
    description = Column(String, unique=False, index=False)
    owner_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)


class Step(Base):
    __tablename__ = 'steps'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=False, index=True)
    description = Column(String, unique=False, index=False)
    order = Column(Integer, unique=False, index=False)
    is_completed = Column(Boolean, unique=False, index=False, default=False)
    checklist_id = Column(Integer, ForeignKey('checklists.id'), nullable=False)
