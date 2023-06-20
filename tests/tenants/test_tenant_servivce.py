import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.exc import DBAPIError
from asyncpg.exceptions import DependentObjectsStillExistError

from opalizer.exceptions import TenantNameNotAvailableError
from opalizer.api.tenants.service import provision_tenant, delete_tenant

@pytest.mark.asyncio
async def cleanup_create_tenant(client: AsyncClient, schema):
    """ Helper to clean up tenant """
    print("clean up", schema)
    result = await delete_tenant(schema, cascade=True)
    assert result == {"schema": schema}


@pytest.mark.asyncio
async def test_create_tenant(client: AsyncClient):
    schema = "test__01"
    result = await provision_tenant(schema=schema)
    assert result == {"schema": schema}
    await cleanup_create_tenant(client, schema)

@pytest.mark.asyncio
async def test_create_tenant_name_not_available(client: AsyncClient):
    try:
        schema = "public"
        result = await provision_tenant(schema=schema)
    except Exception as e:
        assert type(e) == TenantNameNotAvailableError

@pytest.mark.asyncio
async def test_delete_tenant_cascade_true(client: AsyncClient):
    schema = "test__01"
    result = await delete_tenant(schema=schema, cascade=True)
    assert result == {"schema": schema}

@pytest.mark.asyncio
async def test_delete_tenant_cascade_false(client: AsyncClient):
    try:
        schema = "test__01"
        result = await delete_tenant(schema=schema, cascade=False)
        assert result == {"schema": schema}
    except DBAPIError as e:
        if e.orig:
            assert e.orig.sqlstate == DependentObjectsStillExistError.sqlstate
        