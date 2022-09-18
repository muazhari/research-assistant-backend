from uuid import UUID

from app.core.model.entity.web_document import WebDocument
from app.infrastucture.gateway.client.web_document_transaction_service_client import \
    web_document_transaction_service_client


async def find_all() -> [WebDocument]:
    async with await web_document_transaction_service_client.find_all() as response:
        assert response.status == 200
        web_documents: [dict] = await response.json()
        web_document_entities = [WebDocument(**web_document) for web_document in web_documents]
        return web_document_entities


async def find_one_by_id(id: UUID) -> WebDocument:
    async with await web_document_transaction_service_client.find_one_by_id(
            id
    ) as response:
        found_web_document: dict = await response.json()
        found_web_document_entity = WebDocument(**found_web_document)
        return found_web_document_entity


async def create_one(web_document: WebDocument) -> WebDocument:
    async with await web_document_transaction_service_client.save_one(
            web_document.dict()
    ) as response:
        saved_web_document: dict = await response.json()
        saved_web_document_entity = WebDocument(**saved_web_document)
        return saved_web_document_entity


async def update_one_by_id(id: UUID, web_document: WebDocument) -> WebDocument:
    async with await web_document_transaction_service_client.update_one_by_id(
            id,
            web_document.dict()
    ) as response:
        updated_web_document: dict = await response.json()
        updated_web_document_entity = WebDocument(**updated_web_document)
        return updated_web_document_entity


async def delete_one_by_id(id: UUID) -> WebDocument:
    async with await web_document_transaction_service_client.delete_one_by_id(
            id
    ) as response:
        deleted_web_document: dict = await response.json()
        deleted_web_document_entity = WebDocument(**deleted_web_document)
        return deleted_web_document_entity
