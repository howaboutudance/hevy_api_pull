"""Listener for webhook subscriptions POST requests."""

import logging

import fastapi

subscribe_app = fastapi.FastAPI()

_log = logging.getLogger(__name__)


@subscribe_app.get("/health")
async def health_check_get_handler():
    """Health check endpoint."""
    return {"status": "healthy"}


@subscribe_app.post("/webhook")
async def webhook_post_handler(request: fastapi.Request):
    """Webhook endpoint."""
    data = await request.json()
    _log.info("Received webhook data: %s", data)
    return {"status": "success"}


# optional AWS Lambda deployment package logic
try:
    from mangum import Mangum

    handler = Mangum(subscribe_app)
except ImportError:
    handler = None
