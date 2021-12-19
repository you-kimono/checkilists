from sqlalchemy.orm import Session

from . import exceptions, models


async def save_checklist(new_checklist: models.Checklist, database: Session) -> models.Checklist:
    database.add(new_checklist)
    database.commit()
    database.refresh(new_checklist)
    return new_checklist


async def get_checklist_by_id(checklist_id: int, database: Session) -> models.Checklist:
    checklist = database.query(models.Checklist).filter(models.Checklist.id == checklist_id)
    if not checklist.first():
        raise exceptions.InvalidChecklist(checklist_id=checklist_id)
    return checklist.first()
