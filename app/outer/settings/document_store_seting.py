import os

from pydantic import BaseSettings


class DocumentStoreConfig(BaseSettings):
    DOCUMENT_STORE_API_KEY_PINECONE = os.getenv("DOCUMENT_STORE_API_KEY_PINECONE", "")

    class Config:
        env_file = ".env"


document_store_config = DocumentStoreConfig()
