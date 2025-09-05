"""Database connection module."""

import logging

from pymongo import AsyncMongoClient

from app.config import settings

_log = logging.getLogger(__name__)


class MongoConnection:
    """MongoDB connection async context manager."""

    _connection_str = f"mongodb://{settings.mongodb.username}:{settings.mongodb.password}@{settings.mongodb.host}"


    def __init__(self, db_name: str):
        """Initialize the database connection."""
        self._db_name = db_name
        self._client = None

    async def __aenter__(self):
        """Enter the database connection context."""
        self._client = AsyncMongoClient(self._connection_str)
        return self._client[self._db_name]

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the database connection context."""
        if self._client is not None:
            await self._client.close()
