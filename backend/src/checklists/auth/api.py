from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.core import SessionLocal
from auth import models, schemas
from auth import crud
from auth.exceptions import EmailAlreadyTaken, UserNotExisting


router = APIRouter()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def register(request: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        profile = await crud.save_profile(models.User(**request.dict()), db)
        return profile
    except EmailAlreadyTaken:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='email already taken',
        )


@router.delete('/{user_id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        await crud.delete_profile(user_id, db)
        return {}
    except UserNotExisting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'user with id {user_id} not found',
        )


@router.get('/{user_id}', status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        profile = await crud.get_profile(user_id, db)
        return profile
    except UserNotExisting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'user with id {user_id} not found',
        )
