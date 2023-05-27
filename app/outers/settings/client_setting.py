import os

from pydantic import BaseSettings


class ClientSetting(BaseSettings):
    CLIENT_OPEN_AI_HOST: str
    CLIENT_OPEN_AI_PORT: str
    CLIENT_OPEN_AI_URL: str = None

    def __init__(self):
        super().__init__()
        self.CLIENT_OPEN_AI_URL = f"https://{self.CLIENT_OPEN_AI_HOST}:{self.CLIENT_OPEN_AI_PORT}"

    class Config:
        env_file = ".env"
