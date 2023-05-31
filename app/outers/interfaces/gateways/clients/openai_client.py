from app.outers.interfaces.gateways.clients.base_client import BaseClient
from app.outers.settings.open_ai_setting import ClientSetting


class OpenAIClient(BaseClient):
    def __init__(self):
        super().__init__()
        self.client_setting = ClientSetting()
        self.base_url = self.client_setting.CLIENT_OPEN_AI_URL
