from httpx import AsyncClient
from starlette.testclient import TestClient

from app.main import app


def get_async_client():
    return AsyncClient(app=app, base_url="http://test")


def get_test_client():
    return TestClient(app=app)
