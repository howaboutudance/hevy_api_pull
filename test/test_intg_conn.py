"""Integration tests for app.conn module."""

import pytest

from app.conn import Mongo_Conn


@pytest.mark.integration
@pytest.mark.asyncio
async def test_mongo_conn():
    """Test MongoDB connection context manager."""
    async with Mongo_Conn("test_db") as db:
        try:
            await db.create_collection("test_collection")
            assert db.name == "test_db"
            assert "test_collection" in await db.list_collection_names()
        finally:
            await db.drop_collection("test_collection")
            assert "test_collection" not in await db.list_collection_names()
