"""Main application module."""

import logging

from app.db.conn import MongoConnection
from app.db.data import HevyApiRepository

_log = logging.getLogger(__name__)

_hevy_api_repo = HevyApiRepository()

async def pull_all_workouts(page_size: int = 5):
    workouts = await _hevy_api_repo.pull_all_workouts(page_size=page_size)
    await truncate_and_store_workouts(workouts)

async def truncate_and_store_workouts(workouts: list) -> None:
    """Truncate the database and store new workouts.

    :param workouts: A list of workout data to store.
    """
    async with MongoConnection("hevy_db") as db:
        _log.info("Truncating and storing %d workouts", len(workouts))
        await db.workouts.drop()
        if workouts:
            await db.workouts.insert_many(workouts)
        _log.info("Finished storing workouts")
