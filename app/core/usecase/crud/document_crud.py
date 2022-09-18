from uuid import UUID

from app.core.model.entity.document import Document
from app.infrastucture.gateway.client.document_transaction_service_client import document_transaction_service_client


async def find_all() -> [Document]:
    async with await document_transaction_service_client.find_all() as response:
        assert response.status == 200
        documents: [dict] = await response.json()
        document_entities = [Document(**document) for document in documents]
        return document_entities


async def find_one_by_id(id: UUID) -> Document:
    async with await document_transaction_service_client.find_one_by_id(
            id
    ) as response:
        found_document: dict = await response.json()
        found_document_entity = Document(**found_document)
        return found_document_entity
