from app.outer.settings.client_setting import client_setting
from app.outer.interfaces.gateways.client.base_client import BaseClient


class OpenAIClient(BaseClient):
    def __init__(self):
        super().__init__()
        self.base_url = client_setting.CLIENT_OPENAI_URL
