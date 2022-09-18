from uuid import UUID

from app.core.model.entity.document_type import DocumentType
from app.infrastucture.gateway.client.document_type_transaction_service_client import \
    document_type_transaction_service_client


async def find_all() -> [DocumentType]:
    async with await document_type_transaction_service_client.find_all() as response:
        assert response.status == 200
        document_types: [dict] = await response.json()
        document_type_entities = [DocumentType(**document_type) for document_type in document_types]
        return document_type_entities


async def find_one_by_id(id: UUID) -> DocumentType:
    async with await document_type_transaction_service_client.find_one_by_id(
            id
    ) as response:
        found_document_type: dict = await response.json()
        found_document_type_entity = DocumentType(**found_document_type)
        return found_document_type_entity


async def create_one(document_type: DocumentType) -> DocumentType:
    async with await document_type_transaction_service_client.save_one(
            document_type.dict()
    ) as response:
        saved_document_type: dict = await response.json()
        saved_document_type_entity = DocumentType(**saved_document_type)
        return saved_document_type_entity


async def update_one_by_id(id: UUID, document_type: DocumentType) -> DocumentType:
    async with await document_type_transaction_service_client.update_one_by_id(
            id,
            document_type.dict()
    ) as response:
        updated_document_type: dict = await response.json()
        updated_document_type_entity = DocumentType(**updated_document_type)
        return updated_document_type_entity


async def delete_one_by_id(id: UUID) -> DocumentType:
    async with await document_type_transaction_service_client.delete_one_by_id(
            id
    ) as response:
        deleted_document_type: dict = await response.json()
        deleted_document_type_entity = DocumentType(**deleted_document_type)
        return deleted_document_type_entity
