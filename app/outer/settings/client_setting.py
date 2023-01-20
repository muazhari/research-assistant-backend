import os

from pydantic import BaseSettings


class ClientSetting(BaseSettings):
    CLIENT_OPENAI_HOST = os.getenv("CLIENT_SOLOMON_HOST", "localhost")
    CLIENT_OPENAI_PORT = os.getenv("CLIENT_SOLOMON_PORT", "8000")
    CLIENT_OPENAI_URL = f'http://{CLIENT_OPENAI_HOST}:{CLIENT_OPENAI_PORT}'

    class Config:
        env_file = ".env"


client_setting = ClientSetting()
