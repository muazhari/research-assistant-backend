from uuid import UUID

from app.core.model.entity.document import Document
from app.infrastucture.gateway.client.document_transaction_service_client import document_transaction_service_client


def find_all() -> [Document]:
    async with await document_transaction_service_client.find_all() as response:
        assert response.status == 200
        documents: [dict] = await response.json()
        document_entities = [Document(**document) for document in documents]
        return document_entities


def find_one_by_id(id: UUID) -> Document:
    async with await document_transaction_service_client.find_one_by_id(
            id
    ) as response:
        found_document: dict = await response.json()
        found_document_entity = Document(**found_document)
        return found_document_entity


def create_one(document: Document) -> Document:
    async with await document_transaction_service_client.save_one(
            document.dict()
    ) as response:
        saved_document: dict = await response.json()
        saved_document_entity = Document(**saved_document)
        return saved_document_entity


def update_one_by_id(id: UUID, document: Document) -> Document:
    async with await document_transaction_service_client.update_one_by_id(
            id,
            document.dict()
    ) as response:
        updated_document: dict = await response.json()
        updated_document_entity = Document(**updated_document)
        return updated_document_entity


def delete_one_by_id(id: UUID) -> Document:
    async with await document_transaction_service_client.delete_one_by_id(
            id
    ) as response:
        deleted_document: dict = await response.json()
        deleted_document_entity = Document(**deleted_document)
        return deleted_document_entity
