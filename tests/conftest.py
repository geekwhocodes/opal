import pytest
from starlette.testclient import TestClient

from opalizer.main import app


@pytest.fixture(scope='module')
def test_app():

    #app:FastAPI = create_app()

    with TestClient(app=app) as c:

        yield c



    