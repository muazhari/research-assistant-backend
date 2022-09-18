from uuid import UUID

from app.core.model.entity.file_document import FileDocument
from app.infrastucture.gateway.client.file_document_transaction_service_client import \
    file_document_transaction_service_client


async def find_all() -> [FileDocument]:
    async with await file_document_transaction_service_client.find_all() as response:
        assert response.status == 200
        file_documents: [dict] = await response.json()
        file_document_entities = [FileDocument(**file_document) for file_document in file_documents]
        return file_document_entities


async def find_one_by_id(id: UUID) -> FileDocument:
    async with await file_document_transaction_service_client.find_one_by_id(
            id
    ) as response:
        found_file_document: dict = await response.json()
        found_file_document_entity = FileDocument(**found_file_document)
        return found_file_document_entity


async def create_one(file_document: FileDocument) -> FileDocument:
    async with await file_document_transaction_service_client.save_one(
            file_document.dict()
    ) as response:
        saved_file_document: dict = await response.json()
        saved_file_document_entity = FileDocument(**saved_file_document)
        return saved_file_document_entity


async def update_one_by_id(id: UUID, file_document: FileDocument) -> FileDocument:
    async with await file_document_transaction_service_client.update_one_by_id(
            id,
            file_document.dict()
    ) as response:
        updated_file_document: dict = await response.json()
        updated_file_document_entity = FileDocument(**updated_file_document)
        return updated_file_document_entity


async def delete_one_by_id(id: UUID) -> FileDocument:
    async with await file_document_transaction_service_client.delete_one_by_id(
            id
    ) as response:
        deleted_file_document: dict = await response.json()
        deleted_file_document_entity = FileDocument(**deleted_file_document)
        return deleted_file_document_entity
