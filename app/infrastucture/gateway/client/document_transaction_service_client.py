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

    async def save_one(self, document_entity_to_save):
        session = await self.get_client_session()
        return session.post(url=f'/documents', json=document_entity_to_save)

    async def update_one_by_id(self, document_id_to_delete, document_entity_to_update):
        session = await self.get_client_session()
        return session.put(url=f'/documents/{document_id_to_delete}', json=document_entity_to_update)

    async def delete_one_by_id(self, document_id_to_delete):
        session = await self.get_client_session()
        return session.delete(url=f'/documents/{document_id_to_delete}')


document_transaction_service_client = DocumentTransactionServiceClient()
