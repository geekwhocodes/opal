import pytest
from async_asgi_testclient import TestClient
from httpx import Response

from opalizer.api.tenants.schemas import TenantSchema

ORG_ID = 1

@pytest.mark.asyncio
async def test_get_org(aio_client: TestClient):
    test_resp = {'data': {'id': ORG_ID}, 'status': 'success'}
    response:Response = await aio_client.get("/v1/orgs/1")
    assert response.status_code == 200
    resp = response.json()
    assert resp == test_resp


@pytest.mark.asyncio
async def test_create_org(aio_client: TestClient):
    org_name ="Geekwhocodes"
    slug = org_name.lower()
    payload = TenantSchema(name=org_name)
    test_resp = {'error': None, 'status': 'ok', 'value': {'id': '1', 'name': 'Geekwhocodes'}}
    response:Response = await aio_client.post("/v1/tenants/", data=payload.json())
    assert response.status_code == 201
    resp = response.json()
    assert resp == test_resp