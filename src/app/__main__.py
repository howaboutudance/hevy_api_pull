"""Main entry point for the application."""

import argparse
import asyncio
import logging

import uvicorn

from app.app import pull_all_workouts
from app.webhook import subscribe_app

_log = logging.getLogger(__name__)


def setup_parser() -> argparse.Namespace:
    """Setup application parser."""
    parser = argparse.ArgumentParser(description="Application Command Line Interface")
    subparsers = parser.add_subparsers(dest="command")

    serve_parser = subparsers.add_parser("serve", help="Start the webhook server")
    serve_parser.add_argument("--host", type=str, default="0.0.0.0")
    serve_parser.add_argument("--port", type=int, default=8000)

    pull_parser = subparsers.add_parser("pull", help="Pull data from external source")
    pull_parser.add_argument("--page_size", type=int, required=True)

    args = parser.parse_args()
    return args


def main():
    """Main execution function."""
    args = setup_parser()

    match args.command:
        case "serve":
            uvicorn.run(subscribe_app, host=args.host, port=args.port)
        case "pull":
            _log.info("Pull command executed")
            asyncio.run(pull_all_workouts(args.page_size))
        case _:
            _log.error("Unknown command")
            raise SystemExit("Unknown command")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
