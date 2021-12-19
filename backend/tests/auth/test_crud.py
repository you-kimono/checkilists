import pytest

from httpx import AsyncClient
from auth import crud, exceptions, models, schemas


@pytest.fixture
def new_profile() -> schemas.ProfileCreate:
    return schemas.ProfileCreate(
        email='TEST@TEST.COM',
        password='test_password'
    )


class TestSaveProfile:

    @pytest.mark.asyncio
    async def test_save_profile_hashes_password(
            self,
            client: AsyncClient,
            new_profile: schemas.ProfileCreate,
            test_database
    ) -> None:
        profile: models.Profile = await crud.save_profile(
            models.Profile(**new_profile.dict()),
            test_database
        )
        assert new_profile.password != profile.password

    @pytest.mark.asyncio
    async def test_save_profile_saves_email_lowercase(
            self,
            client: AsyncClient,
            new_profile: schemas.ProfileCreate,
            test_database
    ) -> None:
        profile: models.Profile = await crud.save_profile(
            models.Profile(**new_profile.dict()),
            test_database
        )
        assert 'TEST@test.com' == profile.email

    @pytest.mark.asyncio
    async def test_save_profile_duplicate_email_raises_exception(
            self,
            client: AsyncClient,
            new_profile: schemas.ProfileCreate,
            test_database
    ) -> None:
        await crud.save_profile(
            models.Profile(**new_profile.dict()),
            test_database
        )
        with pytest.raises(exceptions.EmailAlreadyTaken):
            await crud.save_profile(
                models.Profile(**new_profile.dict()),
                test_database
            )


class TestGetProfileByID:

    @pytest.mark.asyncio
    async def test_get_profile_returns_expected_entry(
            self,
            client: AsyncClient,
            new_profile: schemas.ProfileCreate,
            test_database
    ) -> None:
        profile: models.Profile = await crud.save_profile(
            models.Profile(**new_profile.dict()),
            test_database
        )
        retrieved_profile: models.Profile = await crud.get_profile_by_id(
            profile.id,
            test_database
        )
        assert profile == retrieved_profile

    @pytest.mark.asyncio
    async def test_get_non_existing_profile_throws_exception(
            self,
            client: AsyncClient,
            new_profile: schemas.ProfileCreate,
            test_database
    ) -> None:
        with pytest.raises(exceptions.InvalidProfile):
            await crud.get_profile_by_id(
                666,
                test_database
            )


class TestGetProfileByEmail:

    @pytest.mark.asyncio
    async def test_get_profile_returns_expected_entry(
            self,
            client: AsyncClient,
            new_profile: schemas.ProfileCreate,
            test_database
    ) -> None:
        profile: models.Profile = await crud.save_profile(
            models.Profile(**new_profile.dict()),
            test_database
        )
        retrieved_profile: models.Profile = await crud.get_profile_by_email(
            profile.email,
            test_database
        )
        assert profile == retrieved_profile

    @pytest.mark.asyncio
    async def test_get_non_existing_profile_throws_exception(
            self,
            client: AsyncClient,
            new_profile: schemas.ProfileCreate,
            test_database
    ) -> None:
        with pytest.raises(exceptions.InvalidProfile):
            await crud.get_profile_by_email(
                'invalid@test.com',
                test_database
            )


class TestDeleteProfile:

    @pytest.mark.asyncio
    async def test_delete_profile_removes_it(
            self,
            client: AsyncClient,
            new_profile: schemas.ProfileCreate,
            test_database
    ) -> None:
        profile: models.Profile = await crud.save_profile(
            models.Profile(**new_profile.dict()),
            test_database
        )
        await crud.delete_profile(profile.id, test_database)
        with pytest.raises(exceptions.InvalidProfile):
            await crud.get_profile_by_id(
                profile.id,
                test_database
            )

    @pytest.mark.asyncio
    async def test_delete_non_existing_profile_throws_exception(
            self,
            client: AsyncClient,
            new_profile: schemas.ProfileCreate,
            test_database
    ) -> None:
        with pytest.raises(exceptions.InvalidProfile):
            await crud.delete_profile(
                666,
                test_database
            )
