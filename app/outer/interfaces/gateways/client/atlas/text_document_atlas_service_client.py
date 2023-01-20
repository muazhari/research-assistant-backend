from app.outer.interfaces.gateways.client.atlas_client import AtlasClient


class TextDocumentAtlasServiceClient(AtlasClient):
    async def find_all(self):
        session = await self.get_client_session()
        return session.get(url=f'/documents/types/texts')

    async def find_one_by_id(self, text_document_id_to_find):
        session = await self.get_client_session()
        return session.get(url=f'/documents/types/texts/{text_document_id_to_find}')

    async def save_one(self, text_document_entity_to_save):
        session = await self.get_client_session()
        return session.post(url=f'/documents/types/texts', json=text_document_entity_to_save)

    async def update_one_by_id(self, text_document_id_to_update, text_document_entity_to_update):
        session = await self.get_client_session()
        return session.put(url=f'/documents/types/texts/{text_document_id_to_update}',
                           json=text_document_entity_to_update)

    async def delete_one_by_id(self, text_document_id_to_delete):
        session = await self.get_client_session()
        return session.delete(url=f'/documents/types/texts/{text_document_id_to_delete}')


text_document_atlas_service_client = TextDocumentAtlasServiceClient()
