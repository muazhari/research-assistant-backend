import aiohttp

from app.infrastucture.config.client_config import client_config
from app.infrastucture.gateway.client.base_client import BaseClient


class DocumentTypeTransactionServiceClient(BaseClient):
    async def find_all(self):
        session = await self.get_client_session()
        return session.get(url=f'/document-types')

    async def find_one_by_id(self, document_type_id_to_find):
        session = await self.get_client_session()
        return session.get(url=f'/document-types/{document_type_id_to_find}')

    async def save_one(self, document_type_entity_to_save):
        session = await self.get_client_session()
        return session.post(url=f'/document-types', json=document_type_entity_to_save)

    async def update_one_by_id(self, document_type_id_to_delete, document_type_entity_to_update):
        session = await self.get_client_session()
        return session.put(url=f'/document-types/{document_type_id_to_delete}',
                           json=document_type_entity_to_update)

    async def delete_one_by_id(self, document_type_id_to_delete):
        session = await self.get_client_session()
        return session.delete(url=f'/document-types/{document_type_id_to_delete}')


document_type_transaction_service_client = DocumentTypeTransactionServiceClient()
