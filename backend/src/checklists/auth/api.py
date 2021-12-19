from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.core import engine, get_db
from . import models, schemas, services
from auth.exceptions import EmailAlreadyTaken, InvalidProfile, LoginFailed


models.Base.metadata.create_all(bind=engine)
router = APIRouter()


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=schemas.Profile)
async def register(request: schemas.ProfileCreate, db: Session = Depends(get_db)):
    try:
        profile = await services.register(models.Profile(**request.dict()), db)
        return profile
    except EmailAlreadyTaken:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='email already taken',
        )


@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    invalid_credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'invalid credentials',
    )
    try:
        return await services.login(request.username, request.password, db)
    except LoginFailed:
        raise invalid_credentials_exception


@router.delete('/profiles/{profile_id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    try:
        return await services.delete_profile_by_id(profile_id, db)
    except InvalidProfile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'profile with id {profile_id} not found',
        )


@router.get('/profiles/{profile_id}', status_code=status.HTTP_200_OK)
async def get_profile(profile_id: int, db: Session = Depends(get_db)):
    try:
        return await services.get_profile_by_id(profile_id, db)
    except InvalidProfile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'profile with id {profile_id} not found',
        )
