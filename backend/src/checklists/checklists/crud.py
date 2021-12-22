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


async def update_checklist(
        updated_checklist: models.Checklist,
        profile_email: str,
        database: Session
) -> models.Checklist:
    db_checklist = await get_checklist_by_id(updated_checklist.id, profile_email, database)
    db_checklist.title = updated_checklist.title
    db_checklist.description = updated_checklist.description
    database.add(db_checklist)
    database.commit()
    database.refresh(db_checklist)
    return db_checklist


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


async def save_step(
        new_step: models.Step,
        checklist_id: int,
        profile_email: str,
        database: Session
) -> models.Checklist:
    await get_checklist_by_id(checklist_id, profile_email, database)

    new_step.checklist_id = checklist_id
    database.add(new_step)
    database.commit()
    database.refresh(new_step)
    return new_step


async def get_step_by_id(step_id: int, checklist_id: int, profile_email: str, database: Session) -> models.Checklist:
    await get_checklist_by_id(checklist_id, profile_email, database)
    step = database.query(models.Step).filter(
        models.Step.id == step_id,
        models.Step.checklist_id == checklist_id
    )
    if not step.first():
        raise exceptions.InvalidStep(step_id=step_id)
    return step.first()


async def get_all_checklist_steps(checklist_id: int, profile_email: str, database: Session) -> List[models.Step]:
    await get_checklist_by_id(checklist_id, profile_email, database)
    steps = database.query(models.Step).filter(
        models.Step.checklist_id == checklist_id
    ).order_by(models.Step.order)
    return steps


async def update_step(step: models.Step, checklist_id: int, profile_email: str, database: Session) -> models.Step:
    db_step: models.Step = await get_step_by_id(step.id, checklist_id, profile_email, database)

    db_step.text = step.text
    db_step.description = step.description
    db_step.order = step.order
    db_step.is_completed = step.is_completed

    database.add(db_step)
    database.commit()
    database.refresh(db_step)

    return db_step


async def delete_step(step_id: int, checklist_id: int, profile_email: str, database: Session) -> None:
    await get_checklist_by_id(checklist_id, profile_email, database)
    step = database.query(models.Step).filter(
        models.Step.id == step_id,
        models.Step.checklist_id == checklist_id
    )
    if not step.first():
        raise exceptions.InvalidStep(step_id=step_id)
    step.delete()
    database.commit()
