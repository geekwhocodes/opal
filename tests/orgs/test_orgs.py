import pytest
from async_asgi_testclient import TestClient
from httpx import Response

ORG_ID = 1

@pytest.mark.asyncio
async def test_get_org(aio_client: TestClient):
    test_resp = {'data': {'id': ORG_ID}, 'status': 'success'}
    response:Response = await aio_client.get("/v1/orgs/1")
    assert response.status_code == 200
    resp = response.json()
    assert resp == test_resp