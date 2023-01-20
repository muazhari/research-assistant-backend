from fastapi.testclient import TestClient

from app.outer.interfaces.gateways.client.openai_client import OpenAIClient
from app.main import app


def get_test_client_app():
    return TestClient(app)


async def get_open_ai_client_session():
    client = OpenAIClient()
    return await client.get_client_session()
