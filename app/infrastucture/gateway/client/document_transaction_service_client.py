import aiohttp

from app.infrastucture.config.client_config import client_config
from app.infrastucture.gateway.client.base_client import BaseClient


class DocumentTransactionServiceClient(BaseClient):
    async def find_all(self):
        session = await self.get_client_session()
        return session.get(url=f'/documents')

    async def find_one_by_id(self, document_id_to_find):
        session = await self.get_client_session()
        return session.get(url=f'/documents/{document_id_to_find}')


document_transaction_service_client = DocumentTransactionServiceClient()
