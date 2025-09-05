"""Tests for app.db.data module."""

from unittest import mock

import httpx
import pytest

from app.db.data import AbstractRestfulApiRepository, HevyApiRepository, JSONType


@pytest.fixture(scope="function", autouse=True)
def httpx_client_fixture():
    """Fixture for httpx.AsyncClient."""

    def _httpx_client(status_code: int, content: JSONType):
        test_client = httpx.AsyncClient(
            transport=httpx.MockTransport(lambda request: httpx.Response(status_code, json=content)),
            base_url="http://localhost/",
        )
        return test_client

    return _httpx_client


@pytest.mark.parametrize("is_closed", [True, False])
def test_abstract_repository_properties(is_closed):
    """Test the properties of the abstract repository."""
    m_url = "http://foo.bar/"
    m_status_code = 200

    class TestRepository(AbstractRestfulApiRepository):
        async def get(self, endpoint: str, params: dict) -> JSONType:
            """Get from the API."""
            return {"data": "test"}

    with mock.patch("app.db.data.httpx.AsyncClient") as m_client:
        m_client.return_value = mock.AsyncMock()
        m_client.return_value.is_closed = is_closed

        m_client_get_response = m_client.return_value.get.return_value = mock.AsyncMock()
        m_client_get_response.status_code = m_status_code

        m_repo = TestRepository(m_url)

        assert m_repo.is_ready is not is_closed
        assert m_repo.base_url == m_url


@pytest.mark.parametrize(
    "http_code, expected_response, except_expected",
    [
        (200, {"workouts": [{"id": 1, "name": "Workout 1"}]}, False),
        (404, {"error": "Not Found"}, True),
    ],
)
@pytest.mark.asyncio
async def test_hevyrepository_pull_all_workouts(http_code, expected_response, except_expected, httpx_client_fixture):
    """Test the pull_all_workouts method of the HevyApiRepository."""
    m_repo = HevyApiRepository()
    m_repo._session = httpx_client_fixture(status_code=http_code, content=expected_response)

    if except_expected:
        with pytest.raises(httpx.HTTPStatusError):
            await m_repo.pull_all_workouts()
    else:
        response = await m_repo.pull_all_workouts()
        assert response == expected_response["workouts"]


@pytest.mark.asyncio
async def test_hevyrepository_get(httpx_client_fixture):
    """Test the get method of the HevyApiRepository."""
    m_response = {"data": "test"}
    m_repo = HevyApiRepository()
    m_repo._session = httpx_client_fixture(status_code=200, content=m_response)

    response = await m_repo.get("/test-endpoint", params={"key": "value"})
    assert response == {"data": "test"}
