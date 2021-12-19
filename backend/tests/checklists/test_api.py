import pytest

from fastapi import status
from httpx import AsyncClient


class TestUnauthenticatedRoutes:

    @pytest.mark.asyncio
    async def test_get_route_is_hidden_behind_authentication(
            self,
            client: AsyncClient
    ) -> None:
        response = await client.get('/checklists/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
