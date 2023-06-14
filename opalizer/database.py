from contextlib import asynccontextmanager
from typing import Union
import logging
from fastapi import Depends
from sqlalchemy import MetaData, select
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from opalizer.api.tenants.models import Tenant
from opalizer.api.tenants.schemas import TenantSchema
from opalizer.models import SharedBase
from opalizer.config import settings

engine = create_async_engine(settings.db_url, echo=bool(settings.sql_echo), pool_pre_ping=True, pool_recycle=240)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION, schema="tenant")
Base = declarative_base(metadata=metadata)

async def create_schema():
    async with engine.begin() as conn:
        await conn.run_sync(SharedBase.metadata.drop_all)
        await conn.run_sync(SharedBase.metadata.create_all)


@asynccontextmanager
async def with_db(tenant_schema_name: Union[str, None]):
    schema_translate_map = None
    if tenant_schema_name:
        schema_translate_map = dict(tenant=tenant_schema_name)
    
    schema_engine = engine.execution_options(schema_translate_map=schema_translate_map)
    try:
        async with async_session(autocommit=False, autoflush=False, bind=schema_engine) as session:
            yield session
    except Exception as e:
        logging.fatal(e, tenant=tenant_schema_name)
        await session.rollback()
    finally:
        await session.close()

async def get_tanant() -> TenantSchema:
    try:
        # get this from the request payload or header
        tenant_name = "gwc"

        if tenant_name is None:
            return None

        tenant_name = tenant_name.strip()

        async with with_db(None) as db:
            query = select(Tenant).where(Tenant.name == tenant_name)
            result = await db.execute(query)

            tenant = result.scalar_one_or_none()

        if tenant is None:
            return None
    except Exception as e:
        logging.fatal(e, tenant=tenant_name)
    return tenant

async def get_db(tenant:Tenant=Depends(get_tanant)):
    if not tenant:
        yield None
    
    async with with_db(tenant.schema) as db:
        yield db

async def get_public_db() -> Session:
    async with with_db("public") as db:
        yield db

        
    
