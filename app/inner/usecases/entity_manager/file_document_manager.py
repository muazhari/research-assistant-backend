import datetime
import uuid
from typing import List
from uuid import UUID

from app.inner.model.entities.file_document import FileDocument
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.file_document.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.file_document.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content
from app.outer.repositories.file_document_repository import file_document_repository


class FileDocumentManager:
    def read_all(self) -> Content[List[FileDocument]]:
        data: FileDocument = file_document_repository.read_all()
        content: Content[List[FileDocument]] = Content[List[FileDocument]](
            message="Read all file_document succeed.",
            data=data
        )
        return content

    def read_one_by_id(self, id: UUID) -> Content[FileDocument]:
        data: FileDocument = file_document_repository.read_one_by_id(id)
        content: Content[FileDocument] = Content[FileDocument](
            message="Read one file_document succeed.",
            data=data
        )
        return content

    def create_one(self, entity_request: CreateOneRequest) -> Content[FileDocument]:
        entity: FileDocument = FileDocument(
            id=uuid.uuid4(),
            document_id=entity_request.document_id,
            file_name=entity_request.file_name,
            file_extension=entity_request.file_extension,
            file_bytes=entity_request.file_bytes
        )

        data: FileDocument = file_document_repository.create_one(entity)
        content: Content[FileDocument] = Content[FileDocument](
            message="Create one file_document succeed.",
            data=data
        )
        return content

    def patch_one_by_id(self, id: UUID, entity_request: PatchOneByIdRequest) -> Content[FileDocument]:
        found_entity: FileDocument = file_document_repository.read_one_by_id(id)

        entity: FileDocument = FileDocument(
            id=found_entity.id,
            document_id=entity_request.document_id,
            file_name=entity_request.file_name,
            file_extension=entity_request.file_extension,
            file_bytes=entity_request.file_bytes
        )

        data: FileDocument = file_document_repository.patch_one_by_id(id, entity)
        content: Content[FileDocument] = Content[FileDocument](
            message="Patch one file_document succeed.",
            data=data
        )
        return content

    def delete_one_by_id(self, id: UUID) -> Content[FileDocument]:
        data: FileDocument = file_document_repository.delete_one_by_id(id)
        content: Content[FileDocument] = Content[FileDocument](
            message="Delete one file_document succeed.",
            data=data
        )
        return content


file_document_manager = FileDocumentManager()
