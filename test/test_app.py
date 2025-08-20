"""Tests for app.app module."""

from unittest import mock

import httpx
import pytest

from app.app import _pull_workouts_page, pull_all_workouts, truncate_and_store_workouts


@pytest.mark.asyncio
async def test_pull_all_workouts():
    """Test pulling all workouts."""
    m_page_size = 5
    m_workout_data = [{"id": idx, "name": f"Workout {idx}"} for idx in range(1, m_page_size + 1)]
    m_test_current_page = 1
    m_truncate_and_store = mock.AsyncMock()
    m_truncate_and_store.return_value = None

    async def test_pull_workout_effect(page: int, page_size: int):
        nonlocal m_test_current_page
        assert page == m_test_current_page
        assert page_size == m_page_size
        data = {
            "workouts": m_workout_data if page <= m_test_current_page else [],
            "page_size": 5 if page <= m_test_current_page else 0,
            "page_count": 1,
            "page": page,
        }
        m_test_current_page += 1
        return data if m_test_current_page == 2 else {}

    m_pull_workouts_page = mock.AsyncMock()
    m_pull_workouts_page.side_effect = test_pull_workout_effect
    with (
        mock.patch("app.app.truncate_and_store_workouts", m_truncate_and_store),
        mock.patch("app.app._pull_workouts_page", m_pull_workouts_page),
    ):
        await pull_all_workouts(page_size=m_page_size)

    m_truncate_and_store.assert_called_once_with(m_workout_data)
    m_pull_workouts_page.assert_awaited()


@pytest.mark.asyncio
async def test_pull_all_workouts_http_error():
    """Test pulling all workouts with HTTP error."""

    async def test_pull_workout_effect(page: int, page_size: int):
        raise httpx.HTTPError("HTTP error")

    m_pull_workouts_page = mock.AsyncMock(side_effect=test_pull_workout_effect)
    with mock.patch("app.app._pull_workouts_page", m_pull_workouts_page):
        with pytest.raises(httpx.HTTPError, match="HTTP error"):
            await pull_all_workouts()


@pytest.mark.asyncio
async def test_truncate_and_store_workouts():
    """Test truncating and storing workouts."""
    m_db = "hevy_db"
    with mock.patch("app.app.Mongo_Conn") as m_conn:
        m_conn.return_value = mock.AsyncMock()
        m_conn.return_value.__aenter__.return_value = m_conn.return_value
        await truncate_and_store_workouts([{"id": 1, "name": "Workout 1"}])
        m_conn.assert_called_once_with(m_db)
        m_conn.return_value.__aenter__.return_value.workouts.insert_many.assert_awaited_once_with(
            [{"id": 1, "name": "Workout 1"}]
        )


@pytest.mark.asyncio
async def test_pull_workouts_page():
    """Test pulling a single page of workouts."""
    with mock.patch("app.app.httpx.AsyncClient", new=mock.AsyncMock()) as m_client:
        m_client.get.return_value.json.return_value = {
            "workouts": [{"id": 1, "name": "Workout 1"}],
            "page_size": 1,
            "page_count": 1,
            "page": 1,
        }
        await _pull_workouts_page(1, 1)
