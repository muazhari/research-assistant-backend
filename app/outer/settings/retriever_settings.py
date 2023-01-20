import os

from pydantic import BaseSettings


class RetrieverSettings(BaseSettings):
    RETRIEVER_OPEN_AI_API_KEY: str = None

    class Config:
        env_file = ".env"


retriever_settings = RetrieverSettings()
