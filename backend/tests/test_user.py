import pytest

from fastapi import status
from httpx import AsyncClient


class TestGetUser:

    @pytest.mark.asyncio
    async def test_get_route_exists(
            self,
            client: AsyncClient
    ) -> None:
        response = await client.get('/users/')
        assert status.HTTP_404_NOT_FOUND != response.status_code
