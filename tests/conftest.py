import pytest
from async_asgi_testclient  import TestClient as AioTestClient
from starlette.testclient import TestClient
import pytest_asyncio
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session

from opalizer.main import app
from opalizer.config import settings
from opalizer.database import get_public_db, get_db, get_tanant


os.environ["ENVIRONMENT"] = "PYTEST"
os.environ["TESTING"] = str("1")
os.environ["SQLALCHEMY_WARN_20"] = "1"


@pytest_asyncio.fixture(name="session")
async def session_fixure():
    engine = create_async_engine(settings.db_test_url, echo=bool(settings.sql_echo), pool_pre_ping=True, pool_recycle=240)
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    schema_translate_map = dict(tenant="fake_tenant_company_for_test_00000000000000000000000000000000")
    schema_engine = engine.execution_options(schema_translate_map=schema_translate_map)
    async with async_session(autocommit=False, autoflush=False, bind=schema_engine) as session:
        yield session



@pytest_asyncio.fixture
async def aio_client(session:Session):
    
    def get_session_override():
        return session
    
    app.dependency_overrides[get_db] = get_session_override
    app.dependency_overrides[get_public_db] = get_session_override

    async with AioTestClient(application=app) as c:
        yield c

@pytest.fixture
def client():
    with TestClient(app=app) as c:
        yield c

    