import os

from pydantic import BaseSettings


class ClientSettings(BaseSettings):
    CLIENT_OPEN_AI_HOST: str = None
    CLIENT_OPEN_AI_PORT: str = None
    CLIENT_OPEN_AI_URL: str = f'http://{CLIENT_OPEN_AI_HOST}:{CLIENT_OPEN_AI_PORT}'

    class Config:
        env_file = ".env"


client_settings = ClientSettings()
