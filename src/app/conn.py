"""Database connection module."""

import logging

from pymongo import AsyncMongoClient

from app.config import settings

_log = logging.getLogger(__name__)


class Mongo_Conn:
    """MongoDB connection async context manager."""

    # import ipdb; ipdb.set_trace()
    _connection_str = f"mongodb://{settings.mongodb.username}:{settings.mongodb.password}@{settings.mongodb.host}"
    _client = AsyncMongoClient(_connection_str)

    def __init__(self, db_name: str):
        """Initialize the database connection."""
        self._db_name = db_name

    async def __aenter__(self):
        """Enter the database connection context."""
        return self._client[self._db_name]

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the database connection context."""
        await self._client.close()
