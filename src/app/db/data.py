"""Repositories for data access."""

import logging
from abc import ABC
from typing import TypeVar

import httpx

from app.config import settings

_log = logging.getLogger(__name__)

# JSONType is a recursive type hint for JSON-compatible data structures
JSONType = TypeVar("None | bool | int | float | str | tuple | list | dict | JSONType")

class RestfulApiRepository(ABC):
    """Abstract base class for RESTful API repositories."""
    def __init__(self, base_url: str):
        """Initialize the repository with a base URL."""
        self._base_url = base_url
        self._session = httpx.AsyncClient(base_url=self._base_url)

    @property
    def base_url(self) -> str:
        """Get the base URL of the repository."""
        return self._base_url

    @property
    def is_ready(self) -> bool:
        """Check if the repository is ready."""
        if self._session.is_closed:
            return False
        response = self._session.get("/")
        return response.status_code == 200

class HevyApiRepository(RestfulApiRepository):
    """Repository for Hevy API."""
    _BASE_URL = f"{settings.hevy_api.url}/{settings.hevy_api.version}"
    _API_KEY = settings.hevy_api.key
    def __init__(self):
        super().__init__(self._BASE_URL)
        self._session.headers.update({"api-key": self._API_KEY})

    # pull workouts with pagination
    async def pull_all_workouts(self, page_size: int = 5) -> JSONType:
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
                data = await self._pull_workouts_page(current_page, page_size)
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
        return workout_data


    async def _pull_workouts_page(self, page: int, page_size: int) -> dict[JSONType]:
        """Pull a single page of workout data.

        :param page: The page number to pull.
        :param page_size: The number of workouts to pull per page.
        :return: The JSON response from the API.
        """
        response = await self._session.get("/workouts", params={"page": page, "pageSize": page_size})
        response.raise_for_status()
        return response.json()