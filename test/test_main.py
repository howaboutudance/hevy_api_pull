"""Tests for app.main module."""

from unittest import mock

import pytest

from app.__main__ import main


@pytest.mark.asyncio
async def test_main():
    """Test main function."""
    with mock.patch("app.__main__.pull_all_workouts", mock.AsyncMock()) as m_pull:
        await main()
        m_pull.assert_called_once()
