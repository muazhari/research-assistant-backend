import os

from pydantic import BaseSettings


class ClientConfig(BaseSettings):
    CLIENT_TRANSACTION_HOST = os.getenv("CLIENT_TRANSACTION_URL", "localhost")
    CLIENT_TRANSACTION_PORT = os.getenv("CLIENT_TRANSACTION_URL", "8080")
    CLIENT_TRANSACTION_URL = f'http://{CLIENT_TRANSACTION_HOST}:{CLIENT_TRANSACTION_PORT}'


client_config = ClientConfig()
