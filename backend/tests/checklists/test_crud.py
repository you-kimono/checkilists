import pytest
from httpx import AsyncClient
from typing import List

from auth import crud as auth_crud, models as auth_models
from checklists import crud, exceptions, models, schemas


@pytest.fixture
def new_checklist() -> schemas.ChecklistCreate:
    return schemas.ChecklistCreate(
        title='test title',
        description='test description'
    )


@pytest.fixture
def new_simple_step() -> schemas.StepCreate:
    return schemas.StepCreate(
        text="step 1",
        description="perform step 1",
        order=0
    )


@pytest.fixture
async def test_user_1(test_database) -> auth_models.Profile:
    user1: auth_models.Profile = auth_models.Profile(
        email='test_user_1@test.com',
        password=''
    )
    return await auth_crud.save_profile(user1, test_database)


@pytest.fixture
async def test_user_2(test_database) -> auth_models.Profile:
    user1: auth_models.Profile = auth_models.Profile(
        email='test_user_2@test.com',
        password=''
    )
    return await auth_crud.save_profile(user1, test_database)


class TestSaveChecklist:

    @pytest.mark.asyncio
    async def test_save_checklist_returns_expected_model(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            test_user_1: auth_models.Profile,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        assert new_checklist.title == checklist.title
        assert new_checklist.description == checklist.description


class TestGetChecklistByID:

    @pytest.mark.asyncio
    async def test_get_checklist_by_id_returns_expected_entry(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            test_user_1: auth_models.Profile,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        retrieved_checklist: models.Checklist = await crud.get_checklist_by_id(
            checklist.id,
            test_user_1.email,
            test_database
        )
        assert checklist == retrieved_checklist

    @pytest.mark.asyncio
    async def test_get_non_existing_checklist_raises_exception(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            test_user_1: auth_models.Profile,
            test_database
    ) -> None:
        with pytest.raises(exceptions.InvalidChecklist):
            await crud.get_checklist_by_id(
                666,
                test_user_1.email,
                test_database
            )

    @pytest.mark.asyncio
    async def test_get_checklist_by_id_of_another_user_raises_exception(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            test_user_1: auth_models.Profile,
            test_user_2: auth_models.Profile,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        with pytest.raises(exceptions.InvalidChecklist):
            await crud.get_checklist_by_id(
                checklist.id,
                test_user_2.email,
                test_database
            )


class TestGetAllChecklists:

    @pytest.mark.asyncio
    async def test_get_all_checklist_returns_expected_entry(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            test_user_1: auth_models.Profile,
            test_user_2: auth_models.Profile,
            test_database
    ) -> None:
        checklist_1: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        checklist_2: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        checklist_3: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_2.email,
            test_database
        )

        retrieved_checklists: List[models.Checklist] = await crud.get_all_checklists(
            test_user_1.email,
            test_database
        )
        assert checklist_1 in retrieved_checklists
        assert checklist_2 in retrieved_checklists
        assert checklist_3 not in retrieved_checklists


class TestDeleteChecklist:

    @pytest.mark.asyncio
    async def test_delete_checklist_removes_it(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            test_user_1: auth_models.Profile,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        await crud.delete_checklist(checklist.id, test_user_1.email, test_database)
        with pytest.raises(exceptions.InvalidChecklist):
            await crud.get_checklist_by_id(
                checklist.id,
                test_user_1.email,
                test_database
            )

    @pytest.mark.asyncio
    async def test_delete_non_existing_checklist_throws_exception(
            self,
            client: AsyncClient,
            test_user_1: auth_models.Profile,
            test_database
    ) -> None:
        with pytest.raises(exceptions.InvalidChecklist):
            await crud.delete_checklist(
                666,
                test_user_1.email,
                test_database
            )

    @pytest.mark.asyncio
    async def test_delete_someone_else_checklist_throws_exception(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            test_user_1: auth_models.Profile,
            test_user_2: auth_models.Profile,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        with pytest.raises(exceptions.InvalidChecklist):
            await crud.delete_checklist(
                checklist.id,
                test_user_2.email,
                test_database
            )


class TestSaveStep:

    @pytest.mark.asyncio
    async def test_save_step_returns_expected_model(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            new_simple_step: schemas.StepCreate,
            test_user_1: auth_models.Profile,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        step: models.Step = await crud.save_step(
            models.Step(**new_simple_step.dict()),
            checklist.id,
            test_user_1.email,
            test_database
        )
        assert new_simple_step.text == step.text
        assert new_simple_step.description == step.description
        assert new_simple_step.order == step.order
        assert not step.is_completed
        assert checklist.id == step.checklist_id


class TestGetStepByID:

    @pytest.mark.asyncio
    async def test_get_step_by_id_returns_expected_entry(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            new_simple_step: schemas.StepCreate,
            test_user_1: auth_models.Profile,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        step: models.Step = await crud.save_step(
            models.Step(**new_simple_step.dict()),
            checklist.id,
            test_user_1.email,
            test_database
        )
        retrieved_step: models.Step = await crud.get_step_by_id(
            step.id,
            checklist.id,
            test_user_1.email,
            test_database
        )
        assert step == retrieved_step

    @pytest.mark.asyncio
    async def test_get_non_existing_step_of_existing_checklist_raises_exception(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            test_user_1: auth_models.Profile,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        with pytest.raises(exceptions.InvalidStep):
            await crud.get_step_by_id(
                666,
                checklist.id,
                test_user_1.email,
                test_database
            )

    @pytest.mark.asyncio
    async def test_get_non_existing_step_of_non_existing_checklist_raises_exception(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            new_simple_step: schemas.StepCreate,
            test_user_1: auth_models.Profile,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        step: models.Step = await crud.save_step(
            models.Step(**new_simple_step.dict()),
            checklist.id,
            test_user_1.email,
            test_database
        )
        with pytest.raises(exceptions.InvalidChecklist):
            await crud.get_step_by_id(
                step.id,
                666,
                test_user_1.email,
                test_database
            )

    @pytest.mark.asyncio
    async def test_get_checklist_by_id_of_another_user_raises_exception(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            new_simple_step: schemas.StepCreate,
            test_user_1: auth_models.Profile,
            test_user_2: auth_models.Profile,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        step: models.Step = await crud.save_step(
            models.Step(**new_simple_step.dict()),
            checklist.id,
            test_user_1.email,
            test_database
        )
        with pytest.raises(exceptions.InvalidChecklist):
            await crud.get_step_by_id(
                step.id,
                checklist.id,
                test_user_2.email,
                test_database
            )


class TestGetAllSteps:

    @pytest.mark.asyncio
    async def test_get_all_steps_returns_expected_entry(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            new_simple_step: schemas.StepCreate,
            test_user_1: auth_models.Profile,
            test_user_2: auth_models.Profile,
            test_database
    ) -> None:
        checklist_1: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        checklist_2: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_2.email,
            test_database
        )
        step_1: models.Step = await crud.save_step(
            models.Step(**new_simple_step.dict()),
            checklist_1.id,
            test_user_1.email,
            test_database
        )
        step_2: models.Step = await crud.save_step(
            models.Step(**new_simple_step.dict()),
            checklist_1.id,
            test_user_1.email,
            test_database
        )
        step_3: models.Step = await crud.save_step(
            models.Step(**new_simple_step.dict()),
            checklist_2.id,
            test_user_2.email,
            test_database
        )

        retrieved_steps: List[models.Step] = await crud.get_all_checklist_steps(
            checklist_1.id,
            test_user_1.email,
            test_database
        )

        assert step_1 in retrieved_steps
        assert step_2 in retrieved_steps
        assert step_3 not in retrieved_steps

    @pytest.mark.asyncio
    async def test_get_all_steps_of_someone_else_checklist_throws_exception(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            new_simple_step: schemas.StepCreate,
            test_user_1: auth_models.Profile,
            test_user_2: auth_models.Profile,
            test_database
    ) -> None:
        checklist_1: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        checklist_2: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_2.email,
            test_database
        )
        await crud.save_step(
            models.Step(**new_simple_step.dict()),
            checklist_1.id,
            test_user_1.email,
            test_database
        )
        await crud.save_step(
            models.Step(**new_simple_step.dict()),
            checklist_2.id,
            test_user_2.email,
            test_database
        )

        with pytest.raises(exceptions.InvalidChecklist):
            await crud.get_all_checklist_steps(
                checklist_1.id,
                test_user_2.email,
                test_database
            )


class TestDeleteStep:

    @pytest.mark.asyncio
    async def test_delete_step_removes_it(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            new_simple_step: schemas.StepCreate,
            test_user_1: auth_models.Profile,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        step: models.Step = await crud.save_step(
            models.Step(**new_simple_step.dict()),
            checklist.id,
            test_user_1.email,
            test_database
        )
        await crud.delete_step(step.id, checklist.id, test_user_1.email, test_database)

        with pytest.raises(exceptions.InvalidStep):
            await crud.get_step_by_id(
                step.id,
                checklist.id,
                test_user_1.email,
                test_database
            )

    @pytest.mark.asyncio
    async def test_delete_non_existing_step_throws_exception(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            test_user_1: auth_models.Profile,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        with pytest.raises(exceptions.InvalidStep):
            await crud.delete_step(
                666,
                checklist.id,
                test_user_1.email,
                test_database
            )

    @pytest.mark.asyncio
    async def test_delete_someone_else_step_throws_exception(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            new_simple_step: schemas.StepCreate,
            test_user_1: auth_models.Profile,
            test_user_2: auth_models.Profile,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        step: models.Step = await crud.save_step(
            models.Step(**new_simple_step.dict()),
            checklist.id,
            test_user_1.email,
            test_database
        )
        with pytest.raises(exceptions.InvalidChecklist):
            await crud.delete_step(
                step.id,
                checklist.id,
                test_user_2.email,
                test_database
            )


class TestUpdateStep:

    @pytest.mark.asyncio
    async def test_update_step(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            new_simple_step: schemas.StepCreate,
            test_user_1: auth_models.Profile,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        step: models.Step = await crud.save_step(
            models.Step(**new_simple_step.dict()),
            checklist.id,
            test_user_1.email,
            test_database
        )
        step.text = "new text 1"
        step.description = "new description 1"
        step.order = 123
        step.is_completed = not step.is_completed

        updated_step: models.Step = await crud.update_step(step, checklist.id, test_user_1.email, test_database)

        assert step.id == updated_step.id
        assert step.text == updated_step.text
        assert step.description == updated_step.description
        assert step.order == updated_step.order
        assert step.is_completed == updated_step.is_completed

    @pytest.mark.asyncio
    async def test_update_someone_else_step_throws_exception(
            self,
            client: AsyncClient,
            new_checklist: schemas.ChecklistCreate,
            new_simple_step: schemas.StepCreate,
            test_user_1: auth_models.Profile,
            test_user_2: auth_models.Profile,
            test_database
    ) -> None:
        checklist: models.Checklist = await crud.save_checklist(
            models.Checklist(**new_checklist.dict()),
            test_user_1.email,
            test_database
        )
        step: models.Step = await crud.save_step(
            models.Step(**new_simple_step.dict()),
            checklist.id,
            test_user_1.email,
            test_database
        )
        with pytest.raises(exceptions.InvalidChecklist):
            await crud.update_step(
                step,
                checklist.id,
                test_user_2.email,
                test_database
            )
