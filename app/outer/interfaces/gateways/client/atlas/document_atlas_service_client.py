from app.outer.interfaces.gateways.client.atlas_client import AtlasClient


class DocumentAtlasServiceClient(AtlasClient):
    async def find_all(self):
        session = await self.get_client_session()
        return session.get(url=f'/documents')

    async def find_one_by_id(self, document_id_to_find):
        session = await self.get_client_session()
        return session.get(url=f'/documents/{document_id_to_find}')


document_atlas_service_client = DocumentAtlasServiceClient()
