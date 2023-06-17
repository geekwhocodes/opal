import asyncio
import pytest
from httpx import AsyncClient
from opalizer.exceptions import TenantNameNotAvailableError
from opalizer.api.tenants.service import provision_tenant, delete_tenant

@pytest.mark.asyncio
async def cleanup_create_tenant(client: AsyncClient, schema):
    """ Helper to clean up tenant """
    print("clean up", schema)
    result = await delete_tenant(schema, cascade=True)
    assert result == {"schema": schema}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "schema",
    (
        (
            "test__01"
        )
    ),
)
async def test_create_tenant(client: AsyncClient, schema):
    result = await provision_tenant(schema=schema)
    assert result == {"schema": schema}
    await cleanup_create_tenant(client, schema)


