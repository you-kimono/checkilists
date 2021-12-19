from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.core import engine, SessionLocal
from auth import models, schemas
from auth import crud
from auth.exceptions import EmailAlreadyTaken, InvalidProfile
from .hashing import Hash
from . import token


models.Base.metadata.create_all(bind=engine)
router = APIRouter()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=schemas.Profile)
async def register(request: schemas.ProfileCreate, db: Session = Depends(get_db)):
    try:
        profile = await crud.save_profile(models.Profile(**request.dict()), db)
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
        profile = await crud.get_profile_by_email(request.username, db)
        if not Hash.verify(profile.password, request.password):
            raise invalid_credentials_exception
        # TODO generate jwt token and return it
        access_token_expires = token.timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = token.create_access_token(
            data={"sub": profile.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except InvalidProfile:
        raise invalid_credentials_exception


@router.delete('/profiles/{profile_id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    try:
        await crud.delete_profile(profile_id, db)
        return {}
    except InvalidProfile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'profile with id {profile_id} not found',
        )


@router.get('/profiles/{profile_id}', status_code=status.HTTP_200_OK)
async def get_profile(profile_id: int, db: Session = Depends(get_db)):
    try:
        profile = await crud.get_profile_by_id(profile_id, db)
        return profile
    except InvalidProfile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'profile with id {profile_id} not found',
        )
