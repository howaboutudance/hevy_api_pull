"""Main applicatiuon module."""

import logging
from typing import TypeVar

import httpx

from app.config import settings
from app.conn import Mongo_Conn

API_KEY = settings.hevy_api.key
BASE_URL = f"{settings.hevy_api.url}/{settings.hevy_api.version}"

_log = logging.getLogger(__name__)
client = httpx.AsyncClient(base_url=BASE_URL, headers={"api-key": API_KEY})

# JSONType is a recursive type hint for JSON-compatible data structures
JSONType = TypeVar("None | bool | int | float | str | tuple | list | dict | JSONType")


# pull workouts with pagination
async def pull_all_workouts(page_size: int = 5):
    """Pull all workout data with pagination.

    :param page_size: The number of workouts to pull per page.
    """
    workout_data = []
    # page field is 1 indexed per:
    # - https://api.hevyapp.com/docs/#/Workouts/PaginatedWorkoutEvents
    current_page = 1

    _log.info("Pulling all workouts with a page_size of %d", page_size)
    # pull pages until len(pages) equils page_count field of json response
    while True:
        try:
            data = await _pull_workouts_page(current_page, page_size)
        except httpx.HTTPError as e:
            _log.error("Error pulling workouts: %s", e)
            raise e
        workouts = data.get("workouts", [])
        workout_data.extend(workouts)
        current_page += 1
        # cover pagination cases
        # - the events array is smaller than the page size
        # - current_page is equal to page_count
        if len(workouts) < page_size or data.get("page_count", 0) < data.get("page", 0):
            break
    _log.info("Finished pulling workouts at %d pages", current_page)
    await truncate_and_store_workouts(workout_data)


async def _pull_workouts_page(page: int, page_size: int) -> dict[JSONType]:
    """Pull a single page of workout data.

    :param page: The page number to pull.
    :param page_size: The number of workouts to pull per page.
    :return: The JSON response from the API.
    """
    response = await client.get("/workouts", params={"page": page, "pageSize": page_size})
    response.raise_for_status()
    return response.json()


async def truncate_and_store_workouts(workouts: list[JSONType]):
    """Truncate the database and store new workouts.

    :param workouts: A list of workout data to store.
    """
    async with Mongo_Conn("hevy_db") as db:
        _log.info("Truncating and storing %d workouts", len(workouts))
        await db.workouts.drop()
        if workouts:
            await db.workouts.insert_many(workouts)
        _log.info("Finished storing workouts")
