import os

from pydantic import BaseSettings


class DocumentStoreSettings(BaseSettings):
    DOCUMENT_STORE_PINECONE_API_KEY: str = None

    class Config:
        env_file = ".env"


document_store_settings = DocumentStoreSettings()
