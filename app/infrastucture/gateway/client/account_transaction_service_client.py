import aiohttp

from app.infrastucture.config.client_config import client_config
from app.infrastucture.gateway.client.BaseClient import BaseClient


class AccountTransactionServiceClient(BaseClient):
    async def find_all(self):
        session = await self.get_client_session()
        return session.get(url=f'/accounts')

    async def find_one_by_id(self, account_id_to_find):
        session = await self.get_client_session()
        return session.get(url=f'/accounts/{account_id_to_find}')

    async def save_one(self, account_entity_to_save):
        session = await self.get_client_session()
        return session.post(url=f'/accounts', json=account_entity_to_save)

    async def update_one_by_id(self, account_id_to_delete, account_entity_to_update):
        session = await self.get_client_session()
        return session.put(url=f'/accounts/{account_id_to_delete}', json=account_entity_to_update)

    async def delete_one_by_id(self, account_id_to_delete):
        session = await self.get_client_session()
        return session.delete(url=f'/accounts/{account_id_to_delete}')


account_transaction_service_client = AccountTransactionServiceClient()
