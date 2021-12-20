from sqlalchemy.orm import Session
from typing import List

from auth import crud
from . import exceptions, models


async def save_checklist(new_checklist: models.Checklist, profile_email: str, database: Session) -> models.Checklist:
    profile = await crud.get_profile_by_email(profile_email, database)
    new_checklist.owner_id = profile.id
    database.add(new_checklist)
    database.commit()
    database.refresh(new_checklist)
    return new_checklist


async def get_checklist_by_id(checklist_id: int, profile_email: str, database: Session) -> models.Checklist:
    profile = await crud.get_profile_by_email(profile_email, database)
    checklist = database.query(models.Checklist).filter(
        models.Checklist.id == checklist_id,
        models.Checklist.owner_id == profile.id
    )
    if not checklist.first():
        raise exceptions.InvalidChecklist(checklist_id=checklist_id)
    return checklist.first()


async def get_all_checklists(profile_email: str, database: Session) -> List[models.Checklist]:
    profile = await crud.get_profile_by_email(profile_email, database)
    checklists = database.query(models.Checklist).filter(
        models.Checklist.owner_id == profile.id
    ).all()
    return checklists


async def delete_checklist(checklist_id: int, profile_email: str, database: Session) -> None:
    profile = await crud.get_profile_by_email(profile_email, database)
    checklist = database.query(models.Checklist).filter(
        models.Checklist.id == checklist_id,
        models.Checklist.owner_id == profile.id
    )
    if not checklist.first():
        raise exceptions.InvalidChecklist(checklist_id=checklist_id)
    checklist.delete()
    database.commit()
