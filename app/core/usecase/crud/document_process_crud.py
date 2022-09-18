from uuid import UUID

from app.core.model.entity.document_process import DocumentProcess
from app.infrastucture.gateway.client.document_process_transaction_service_client import \
    document_process_transaction_service_client


async def find_all() -> [DocumentProcess]:
    async with await document_process_transaction_service_client.find_all() as response:
        assert response.status == 200
        document_processes: [dict] = await response.json()
        document_process_entities = [DocumentProcess(**document_process) for document_process in document_processes]
        return document_process_entities


async def find_one_by_id(id: UUID) -> DocumentProcess:
    async with await document_process_transaction_service_client.find_one_by_id(
            id
    ) as response:
        found_document_process: dict = await response.json()
        found_document_process_entity = DocumentProcess(**found_document_process)
        return found_document_process_entity


async def create_one(document_process: DocumentProcess) -> DocumentProcess:
    async with await document_process_transaction_service_client.save_one(
            document_process.dict()
    ) as response:
        saved_document_process: dict = await response.json()
        saved_document_process_entity = DocumentProcess(**saved_document_process)
        return saved_document_process_entity


async def update_one_by_id(id: UUID, document_process: DocumentProcess) -> DocumentProcess:
    async with await document_process_transaction_service_client.update_one_by_id(
            id,
            document_process.dict()
    ) as response:
        updated_document_process: dict = await response.json()
        updated_document_process_entity = DocumentProcess(**updated_document_process)
        return updated_document_process_entity


async def delete_one_by_id(id: UUID) -> DocumentProcess:
    async with await document_process_transaction_service_client.delete_one_by_id(
            id
    ) as response:
        deleted_document_process: dict = await response.json()
        deleted_document_process_entity = DocumentProcess(**deleted_document_process)
        return deleted_document_process_entity
