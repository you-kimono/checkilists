import pytest

from httpx import AsyncClient
from auth import crud, exceptions, models, schemas


@pytest.fixture
def new_user() -> schemas.UserCreate:
    return schemas.UserCreate(
        email='TEST@TEST.COM',
        password='test_password'
    )


class TestSaveProfile:

    @pytest.mark.asyncio
    async def test_save_profile_hashes_password(
            self,
            client: AsyncClient,
            new_user: schemas.UserCreate,
            test_database
    ) -> None:
        profile: models.User = await crud.save_profile(
            models.User(**new_user.dict()),
            test_database
        )
        assert new_user.password != profile.password

    @pytest.mark.asyncio
    async def test_save_profile_saves_email_lowercase(
            self,
            client: AsyncClient,
            new_user: schemas.UserCreate,
            test_database
    ) -> None:
        profile: models.User = await crud.save_profile(
            models.User(**new_user.dict()),
            test_database
        )
        assert 'TEST@test.com' == profile.email

    @pytest.mark.asyncio
    async def test_save_profile_duplicate_email_raises_exception(
            self,
            client: AsyncClient,
            new_user: schemas.UserCreate,
            test_database
    ) -> None:
        await crud.save_profile(
            models.User(**new_user.dict()),
            test_database
        )
        with pytest.raises(exceptions.EmailAlreadyTaken):
            await crud.save_profile(
                models.User(**new_user.dict()),
                test_database
            )


class TestGetProfile:

    @pytest.mark.asyncio
    async def test_get_profile_returns_expected_entry(
            self,
            client: AsyncClient,
            new_user: schemas.UserCreate,
            test_database
    ) -> None:
        profile: models.User = await crud.save_profile(
            models.User(**new_user.dict()),
            test_database
        )
        retrieved_profile: models.User = await crud.get_profile(
            profile.id,
            test_database
        )
        assert profile == retrieved_profile

    @pytest.mark.asyncio
    async def test_get_non_existing_profile_throws_exception(
            self,
            client: AsyncClient,
            new_user: schemas.UserCreate,
            test_database
    ) -> None:
        with pytest.raises(exceptions.UserNotExisting):
            await crud.get_profile(
                666,
                test_database
            )


class TestDeleteProfile:

    @pytest.mark.asyncio
    async def test_delete_profile_removes_it(
            self,
            client: AsyncClient,
            new_user: schemas.UserCreate,
            test_database
    ) -> None:
        profile: models.User = await crud.save_profile(
            models.User(**new_user.dict()),
            test_database
        )
        await crud.delete_profile(profile.id, test_database)
        with pytest.raises(exceptions.UserNotExisting):
            await crud.get_profile(
                profile.id,
                test_database
            )

    @pytest.mark.asyncio
    async def test_delete_non_existing_profile_throws_exception(
            self,
            client: AsyncClient,
            new_user: schemas.UserCreate,
            test_database
    ) -> None:
        with pytest.raises(exceptions.UserNotExisting):
            await crud.delete_profile(
                666,
                test_database
            )
