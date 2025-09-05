"""Tests for app.db.data module."""

from unittest import mock

import pytest

from app.db.data import HevyApiRepository


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
