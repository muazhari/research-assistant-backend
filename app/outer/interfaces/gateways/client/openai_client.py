from app.outer.interfaces.gateways.client.base_client import BaseClient
from app.outer.settings.client_settings import client_settings


class OpenAIClient(BaseClient):
    def __init__(self):
        super().__init__()
        self.base_url = client_settings.CLIENT_OPENAI_URL
