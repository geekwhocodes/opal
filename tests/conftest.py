import pytest
from async_asgi_testclient  import TestClient as AioTestClient
from starlette.testclient import TestClient
import pytest_asyncio

from opalizer.main import app


@pytest_asyncio.fixture
async def aio_client():
    async with AioTestClient(application=app) as c:
        yield c


@pytest.fixture
def client():
    with TestClient(app=app) as c:
        yield c

    