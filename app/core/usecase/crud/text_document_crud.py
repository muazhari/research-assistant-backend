from uuid import UUID

from app.core.model.entity.text_document import TextDocument
from app.infrastucture.gateway.client.text_document_transaction_service_client import \
    text_document_transaction_service_client


def find_all() -> [TextDocument]:
    async with await text_document_transaction_service_client.find_all() as response:
        assert response.status == 200
        text_documents: [dict] = await response.json()
        text_document_entities = [TextDocument(**text_document) for text_document in text_documents]
        return text_document_entities


def find_one_by_id(id: UUID) -> TextDocument:
    async with await text_document_transaction_service_client.find_one_by_id(
            id
    ) as response:
        found_text_document: dict = await response.json()
        found_text_document_entity = TextDocument(**found_text_document)
        return found_text_document_entity


def create_one(text_document: TextDocument) -> TextDocument:
    async with await text_document_transaction_service_client.save_one(
            text_document.dict()
    ) as response:
        saved_text_document: dict = await response.json()
        saved_text_document_entity = TextDocument(**saved_text_document)
        return saved_text_document_entity


def update_one_by_id(id: UUID, text_document: TextDocument) -> TextDocument:
    async with await text_document_transaction_service_client.update_one_by_id(
            id,
            text_document.dict()
    ) as response:
        updated_text_document: dict = await response.json()
        updated_text_document_entity = TextDocument(**updated_text_document)
        return updated_text_document_entity


def delete_one_by_id(id: UUID) -> TextDocument:
    async with await text_document_transaction_service_client.delete_one_by_id(
            id
    ) as response:
        deleted_text_document: dict = await response.json()
        deleted_text_document_entity = TextDocument(**deleted_text_document)
        return deleted_text_document_entity
