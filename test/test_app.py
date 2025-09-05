"""Tests for app.app module."""

from unittest import mock

import pytest

from app.app import pull_all_workouts, truncate_and_store_workouts
from app.db.data import HevyApiRepository


@pytest.mark.asyncio
async def test_pull_all_workouts():
    """Test pulling all workouts."""
    m_response = {"workouts": [{"id": 1, "name": "Workout 1"}]}
    with (
        mock.patch.object(HevyApiRepository, "pull_all_workouts") as m_repo,
        mock.patch("app.app.truncate_and_store_workouts", mock.AsyncMock()) as m_store,
    ):
        m_repo.return_value = m_response
        await pull_all_workouts()

        m_store.assert_awaited_once_with(m_response)


@pytest.mark.asyncio
async def test_truncate_and_store_workouts():
    """Test truncating and storing workouts."""
    m_db = "hevy_db"
    with mock.patch("app.app.MongoConnection") as m_conn:
        m_conn.return_value = mock.AsyncMock()
        m_conn.return_value.__aenter__.return_value = m_conn.return_value
        await truncate_and_store_workouts([{"id": 1, "name": "Workout 1"}])
        m_conn.assert_called_once_with(m_db)
        m_conn.return_value.__aenter__.return_value.workouts.insert_many.assert_awaited_once_with(
            [{"id": 1, "name": "Workout 1"}]
        )
