import aiohttp

from app.infrastucture.config.client_config import client_config
from app.infrastucture.gateway.client.base_client import BaseClient


class DocumentProcessTransactionServiceClient(BaseClient):
    async def find_all(self):
        session = await self.get_client_session()
        return session.get(url=f'/document-processes')

    async def find_one_by_id(self, document_process_id_to_find):
        session = await self.get_client_session()
        return session.get(url=f'/document-processes/{document_process_id_to_find}')

    async def save_one(self, document_process_entity_to_save):
        session = await self.get_client_session()
        return session.post(url=f'/document-processes', json=document_process_entity_to_save)

    async def update_one_by_id(self, document_process_id_to_delete, document_process_entity_to_update):
        session = await self.get_client_session()
        return session.put(url=f'/document-processes/{document_process_id_to_delete}',
                           json=document_process_entity_to_update)

    async def delete_one_by_id(self, document_process_id_to_delete):
        session = await self.get_client_session()
        return session.delete(url=f'/document-processes/{document_process_id_to_delete}')


document_process_transaction_service_client = DocumentProcessTransactionServiceClient()