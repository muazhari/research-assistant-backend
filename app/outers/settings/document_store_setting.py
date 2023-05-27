import os

from pydantic import BaseSettings


class DocumentStoreSetting(BaseSettings):
    DOCUMENT_STORE_PINECONE_API_KEY: str

    class Config:
        env_file = ".env"
