import pytest

from httpx import AsyncClient
from checklists import crud, exceptions, models, schemas


@pytest.fixture
def new_checklist() -> schemas.ChecklistCreate:
    return schemas.ChecklistCreate(
        title='test title',
        description='test description'
    )


class TestSaveChecklist:

    @pytest.mark.asyncio
    async def test_save_checklist_returns_expected_model(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_database
        )
        assert new_checklist.title == checklist.title
        assert new_checklist.description == checklist.description


class TestGetProfileByID:

    @pytest.mark.asyncio
    async def test_get_checklist_by_id_returns_expected_entry(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_database
        )
        retrieved_checklist: models.Checklist = await crud.get_checklist_by_id(
            checklist.id,
            test_database
        )
        assert checklist == retrieved_checklist

    @pytest.mark.asyncio
    async def test_get_non_existing_checklist_raises_exception(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            test_database
    ) -> None:
        with pytest.raises(exceptions.InvalidChecklist):
            await crud.get_checklist_by_id(
                666,
                test_database
            )
