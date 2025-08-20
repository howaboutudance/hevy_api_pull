"""Main entry point for the application."""

import asyncio
import logging

from app.app import pull_all_workouts

_log = logging.getLogger(__name__)


async def main():
    """Main execution function."""
    _log.info("starting workout batch job")
    await pull_all_workouts()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
