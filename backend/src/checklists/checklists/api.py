from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.core import engine, get_db
from auth import schemas as auth_schemas
from auth import oauth2
from . import exceptions, models, schemas, services


models.Base.metadata.create_all(bind=engine)
router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.Checklist])
async def get_all_checklists(
        db: Session = Depends(get_db),
        profile: auth_schemas.TokenData = Depends(oauth2.get_current_user)
):
    response = await services.get_all_checklists(profile, db)
    return response


@router.get('/{checklist_id}', status_code=status.HTTP_200_OK)
async def get_checklist(
        checklist_id: int,
        db: Session = Depends(get_db),
        profile: auth_schemas.TokenData = Depends(oauth2.get_current_user)
):
    try:
        return await services.get_checklist_by_id(checklist_id, profile, db)
    except exceptions.InvalidChecklist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'checklist with id {checklist_id} not found',
        )


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Checklist)
async def create_checklist(
        request: schemas.ChecklistCreate,
        db: Session = Depends(get_db),
        profile: auth_schemas.TokenData = Depends(oauth2.get_current_user)
):
    checklist = await services.create_checklist(models.Checklist(**request.dict()), profile, db)
    return checklist


@router.delete('/{checklist_id}', status_code=status.HTTP_202_ACCEPTED)
async def get_checklist(
        checklist_id: int,
        db: Session = Depends(get_db),
        profile: auth_schemas.TokenData = Depends(oauth2.get_current_user)
):
    try:
        return await services.delete_checklist(checklist_id, profile, db)
    except exceptions.InvalidChecklist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'checklist with id {checklist_id} not found',
        )


@router.post('/{checklist_id}/steps', status_code=status.HTTP_201_CREATED, response_model=schemas.Step)
async def create_step(
        checklist_id: int,
        request: schemas.StepCreate,
        db: Session = Depends(get_db),
        profile: auth_schemas.TokenData = Depends(oauth2.get_current_user)
):
    step = await services.create_step(models.Step(**request.dict()), checklist_id, profile, db)
    return step


@router.get('/{checklist_id}/steps', status_code=status.HTTP_200_OK, response_model=schemas.Step)
async def get_step(
        checklist_id: int,
        step_id: int,
        db: Session = Depends(get_db),
        profile: auth_schemas.TokenData = Depends(oauth2.get_current_user)
):
    try:
        step = await services.get_step_by_id(step_id, checklist_id, profile, db)
        return step
    except (exceptions.InvalidStep, exceptions.InvalidChecklist):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'the resource you were looking for does not exist',
        )


@router.get('/{checklist_id}/steps/{step_id}', status_code=status.HTTP_200_OK, response_model=schemas.Step)
async def get_step(
        checklist_id: int,
        step_id: int,
        db: Session = Depends(get_db),
        profile: auth_schemas.TokenData = Depends(oauth2.get_current_user)
):
    try:
        step = await services.get_step_by_id(step_id, checklist_id, profile, db)
        return step
    except (exceptions.InvalidStep, exceptions.InvalidChecklist):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'the resource you were looking for does not exist',
        )


@router.delete('/{checklist_id}/steps/{step_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Step)
async def delete_step(
        checklist_id: int,
        step_id: int,
        db: Session = Depends(get_db),
        profile: auth_schemas.TokenData = Depends(oauth2.get_current_user)
):
    try:
        step = await services.delete_step(step_id, checklist_id, profile, db)
        return step
    except (exceptions.InvalidStep, exceptions.InvalidChecklist):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'the resource you were looking for does not exist',
        )
