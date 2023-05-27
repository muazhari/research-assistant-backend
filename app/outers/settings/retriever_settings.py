from pydantic import BaseSettings


class RetrieverSettings(BaseSettings):
    RETRIEVER_OPEN_AI_API_KEY: str

    class Config:
        env_file = ".env"
