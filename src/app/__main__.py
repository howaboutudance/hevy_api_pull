"""Main entry point for the application."""

import asyncio
import logging

from app.app import pull_all_workouts

_log = logging.getLogger(__name__)


def main():
    """Main execution function."""
    _log.info("starting workout batch job")
    asyncio.run(pull_all_workouts())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
