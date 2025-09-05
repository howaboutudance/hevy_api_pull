"""Tests for app.conn module."""

import pytest

from app.db.conn import MongoConnection


# test Mongo_Conn as a context manager
@pytest.mark.asyncio
async def test_mongo_conn():
    """Test MongoDB connection context manager."""
    async with MongoConnection("test_db") as db:
        assert db.name == "test_db"
