"""Tests for app.conn module."""

import pytest

from app.conn import Mongo_Conn


# test Mongo_Conn as a context manager
@pytest.mark.asyncio
async def test_mongo_conn():
    """Test MongoDB connection context manager."""
    async with Mongo_Conn("test_db") as db:
        assert db.name == "test_db"
