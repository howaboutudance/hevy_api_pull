"""Integration tests for api client module."""
import asyncio
import socket
import threading

import httpx
import pytest
import uvicorn

from app.webhook import subscribe_app

pytestmark = [pytest.mark.integration]
LOCAL_IP = "127.0.0.1"


@pytest.fixture(scope="session", autouse=True)
def socket_port_fixture():
    """A fixture to create a socket port for the FastAPI server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

@pytest.fixture(scope="session")
def app_server_fixture(socket_port_fixture):
    """A fixture to run a FastAPI server on a seperate thread."""
    url = f"http://{LOCAL_IP}:{socket_port_fixture}"
    config = uvicorn.Config(subscribe_app, host=LOCAL_IP, port=socket_port_fixture, log_level="info")
    server = uvicorn.Server(config=config)

    # we need a health check to prevent the url being yielded before the server
    # has fully started
    async def wait_for_health_check():
        async with httpx.AsyncClient() as client:
            while True:
                try:
                    response = await client.get(f"{url}/health")
                    if response.status_code == 200:
                        break
                except httpx.HTTPError:
                    pass
                await asyncio.sleep(0.1)

    server_thread = threading.Thread(target=asyncio.run, args=(server.serve(),))
    server_thread.start()

    asyncio.run(wait_for_health_check())

    yield url

    server.should_exit = True
    server_thread.join()


# A integration test that will send a post request to a endpoint
# used to subscribe to a webhook and recieve a request with the
# json body of:
# ```json
# {
#   "id": "00000000-0000-0000-0000-000000000001",
#   "payload": {
#     "workoutId": "f1085cdb-32b2-4003-967d-53a3af8eaecb"
#   }
# } 
# ```
def test_webhook_endpoiont_recieves_data(app_server_fixture):
    """Test that the webhook endpoint recieves data."""
    data = {
        "id": "00000000-0000-0000-0000-000000000001",
        "payload": {
            "workoutId": "f1085cdb-32b2-4003-967d-53a3af8eaecb"
        }
    }
    url = f"{app_server_fixture}/webhook"

    response = httpx.post(url, json=data)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}