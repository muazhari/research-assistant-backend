from app.outer.interfaces.gateways.client.atlas_client import AtlasClient


class WebDocumentAtlasServiceClient(AtlasClient):
    async def find_all(self):
        session = await self.get_client_session()
        return session.get(url=f'/documents/types/webs')

    async def find_one_by_id(self, web_document_id_to_find):
        session = await self.get_client_session()
        return session.get(url=f'/documents/types/webs/{web_document_id_to_find}')

    async def save_one(self, web_document_entity_to_save):
        session = await self.get_client_session()
        return session.post(url=f'/documents/types/webs', json=web_document_entity_to_save)

    async def update_one_by_id(self, web_document_id_to_update, web_document_entity_to_update):
        session = await self.get_client_session()
        return session.put(url=f'/documents/types/webs/{web_document_id_to_update}',
                           json=web_document_entity_to_update)

    async def delete_one_by_id(self, web_document_id_to_delete):
        session = await self.get_client_session()
        return session.delete(url=f'/documents/types/webs/{web_document_id_to_delete}')


web_document_atlas_service_client = WebDocumentAtlasServiceClient()
