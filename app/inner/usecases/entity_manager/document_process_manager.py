import datetime
import uuid
from typing import List
from uuid import UUID

from app.inner.model.entities.document_process import DocumentProcess
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document_process.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document_process.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content
from app.outer.repositories.document_process_repository import document_process_repository


class DocumentProcessManager:
    def read_all(self) -> Content[List[DocumentProcess]]:
        data: DocumentProcess = document_process_repository.read_all()
        content: Content[List[DocumentProcess]] = Content[List[DocumentProcess]](
            message="Read all document_process succeed.",
            data=data
        )
        return content

    def read_one_by_id(self, id: UUID) -> Content[DocumentProcess]:
        data: DocumentProcess = document_process_repository.read_one_by_id(id)
        content: Content[DocumentProcess] = Content[DocumentProcess](
            message="Read one document_process by id succeed.",
            data=data
        )
        return content

    def create_one(self, entity_request: CreateOneRequest) -> Content[DocumentProcess]:
        entity: DocumentProcess = DocumentProcess(
            id=uuid.uuid4(),
            initial_document_id=entity_request.initial_document_id,
            final_document_id=entity_request.final_document_id,
            process_duration=entity_request.process_duration,
            updated_at=datetime.datetime.now(),
            created_at=datetime.datetime.now(),
        )

        data: DocumentProcess = document_process_repository.create_one(entity)
        content: Content[DocumentProcess] = Content[DocumentProcess](
            message="Create one document_process succeed.",
            data=data
        )
        return content

    def patch_one_by_id(self, id: UUID, entity_request: PatchOneByIdRequest) -> Content[DocumentProcess]:
        found_entity: DocumentProcess = document_process_repository.read_one_by_id(id)

        entity: DocumentProcess = DocumentProcess(
            id=found_entity.id,
            initial_document_id=entity_request.initial_document_id,
            final_document_id=entity_request.final_document_id,
            process_duration=entity_request.process_duration,
            updated_at=datetime.datetime.now(),
            created_at=found_entity.created_at,
        )

        data: DocumentProcess = document_process_repository.patch_one_by_id(id, entity)
        content: Content[DocumentProcess] = Content[DocumentProcess](
            message="Patch one document_process by id succeed.",
            data=data
        )
        return content

    def delete_one_by_id(self, id: UUID) -> Content[DocumentProcess]:
        data: DocumentProcess = document_process_repository.delete_one_by_id(id)
        content: Content[DocumentProcess] = Content[DocumentProcess](
            message="Delete one document_process by id succeed.",
            data=data
        )
        return content


document_process_manager = DocumentProcessManager()
