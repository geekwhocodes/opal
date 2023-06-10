from starlette.testclient import TestClient
from httpx import Response

def test_ping(test_app: TestClient):
    response:Response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == 1