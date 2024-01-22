from httpx import AsyncClient

from app.main import app


def get_async_client():
    return AsyncClient(app=app, base_url="http://test")
