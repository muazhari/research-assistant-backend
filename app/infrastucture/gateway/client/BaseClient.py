import aiohttp

from app.infrastucture.config.client_config import client_config


class BaseClient:
    async def get_client_session(self):
        return aiohttp.ClientSession(base_url=client_config.CLIENT_TRANSACTION_URL)
