import datetime
import uuid
from typing import List
from uuid import UUID

from app.inner.model.entities.document_type import DocumentType
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document_type.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document_type.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content
from app.outer.repositories.document_type_repository import document_type_repository


class DocumentTypeManager:
    def read_all(self) -> Content[List[DocumentType]]:
        data: DocumentType = document_type_repository.read_all()
        content: Content[List[DocumentType]] = Content[List[DocumentType]](
            message="Read all document_type succeed.",
            data=data
        )
        return content

    def read_one_by_id(self, id: UUID) -> Content[DocumentType]:
        data: DocumentType = document_type_repository.read_one_by_id(id)
        content: Content[DocumentType] = Content[DocumentType](
            message="Read one document_type by id succeed.",
            data=data
        )
        return content

    def create_one(self, entity_request: CreateOneRequest) -> Content[DocumentType]:
        entity: DocumentType = DocumentType(
            id=uuid.uuid4(),
            name=entity_request.name,
            description=entity_request.description,
            updated_at=datetime.datetime.now(),
            created_at=datetime.datetime.now(),
        )

        data: DocumentType = document_type_repository.create_one(entity)
        content: Content[DocumentType] = Content[DocumentType](
            message="Create one document_type succeed.",
            data=data
        )
        return content

    def patch_one_by_id(self, id: UUID, entity_request: PatchOneByIdRequest) -> Content[DocumentType]:
        found_entity: DocumentType = document_type_repository.read_one_by_id(id)

        entity: DocumentType = DocumentType(
            id=found_entity.id,
            name=entity_request.name,
            description=entity_request.description,
            updated_at=datetime.datetime.now(),
            created_at=found_entity.created_at,
        )

        data: DocumentType = document_type_repository.patch_one_by_id(id, entity)
        content: Content[DocumentType] = Content[DocumentType](
            message="Patch one document_type by id succeed.",
            data=data
        )
        return content

    def delete_one_by_id(self, id: UUID) -> Content[DocumentType]:
        data: DocumentType = document_type_repository.delete_one_by_id(id)
        content: Content[DocumentType] = Content[DocumentType](
            message="Delete one document_type by id succeed.",
            data=data
        )
        return content


document_type_manager = DocumentTypeManager()
