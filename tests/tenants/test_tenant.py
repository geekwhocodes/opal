import pytest
from async_asgi_testclient import TestClient
from httpx import Response, _status_codes

from opalizer.api.tenants.schemas import TenantSchema, TenantSchemaIn

@pytest.mark.asyncio
async def test_get_all_tenants(client: TestClient):
    response:Response = await client.get("/v1/tenants/")
    assert response.status_code == _status_codes.code.OK
    resp = response.json()
    assert resp.get("status") == "success"
    assert isinstance(resp.get("value"), list)


@pytest.mark.asyncio
async def test_create_tenant(client: TestClient):
    org_name ="kabo"
    payload = TenantSchemaIn(name=org_name)
    response:Response = await client.post("/v1/tenants/", data=payload.json())
    assert response.status_code == _status_codes.code.OK
    resp = response.json()
    assert resp.get("status") == "success"
    result = TenantSchema(**resp.get("value"))
    assert isinstance(result, TenantSchema)
    assert result.name == org_name