"""Tests for app.db.data module."""

from unittest import mock

import pytest

from app.db.data import HevyApiRepository, AbstractRestfulApiRepository


@pytest.mark.parametrize(
        "is_closed",
        [True, False]
)
def test_abstract_repository_properties(is_closed):
    m_url = "http://foo.bar/"
    m_status_code = 200
    with mock.patch("app.db.data.httpx.AsyncClient") as m_client:
        m_client.return_value = mock.AsyncMock()
        m_client.return_value.is_closed = is_closed

        m_client_get_response = m_client.return_value.get.return_value = mock.AsyncMock()
        m_client_get_response.status_code = m_status_code

        m_repo = AbstractRestfulApiRepository(m_url)

        assert m_repo.is_ready is not is_closed
        assert m_repo.base_url == m_url

## HevyApiRepository Tests
class HevyApiTestRepository(HevyApiRepository):
    def __init__(self):
        super().__init__()
        self._session = mock.AsyncMock()
        self._session.get = mock.AsyncMock()


@pytest.mark.asyncio
async def test_pull_workouts_page():
    """Test pulling a single page of workouts."""
    m_repo = HevyApiTestRepository()
    m_repo._session.get.return_value.json.return_value = {
        "workouts": [{"id": 1, "name": "Workout 1"}],
        "page_size": 1,
        "page_count": 1,
        "page": 1,
    }

    await m_repo._pull_workouts_page(1, 1)



