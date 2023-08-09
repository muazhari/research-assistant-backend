from app.outers.interfaces.gateways.clients.base_client import BaseClient
from app.outers.settings.openai_setting import OpenAiSetting


class OpenAiClient(BaseClient):
    def __init__(
            self,
            openai_setting: OpenAiSetting
    ):
        super().__init__(
            base_url=openai_setting.OPEN_AI_URL
        )
        self.openai_setting = openai_setting
