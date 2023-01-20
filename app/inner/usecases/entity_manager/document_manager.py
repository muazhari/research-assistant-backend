import datetime
import uuid
from typing import List
from uuid import UUID

from app.inner.model.entities.document import Document
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content
from app.outer.repositories.document_repository import document_repository


class DocumentManager:
    def read_all(self) -> Content[List[Document]]:
        data: Document = document_repository.read_all()
        content: Content[List[Document]] = Content[List[Document]](
            message="Read all document succeed.",
            data=data
        )
        return content

    def read_one_by_id(self, id: UUID) -> Content[Document]:
        data: Document = document_repository.read_one_by_id(id)
        content: Content[Document] = Content[Document](
            message="Read one document succeed.",
            data=data
        )
        return content

    def create_one(self, entity_request: CreateOneRequest) -> Content[Document]:
        entity: Document = Document(
            id=uuid.uuid4(),
            name=entity_request.name,
            description=entity_request.description,
            document_type_id=entity_request.document_type_id,
            account_id=entity_request.account_id,
            updated_at=datetime.datetime.now(),
            created_at=datetime.datetime.now(),
        )

        data: Document = document_repository.create_one(entity)
        content: Content[Document] = Content[Document](
            message="Create one document succeed.",
            data=data
        )
        return content

    def patch_one_by_id(self, id: UUID, entity_request: PatchOneByIdRequest) -> Content[Document]:
        found_entity: Document = document_repository.read_one_by_id(id)

        entity: Document = Document(
            id=found_entity.id,
            name=entity_request.name,
            description=entity_request.description,
            document_type_id=entity_request.document_type_id,
            account_id=entity_request.account_id,
            updated_at=datetime.datetime.now(),
            created_at=found_entity.created_at,
        )

        data: Document = document_repository.patch_one_by_id(id, entity)
        content: Content[Document] = Content[Document](
            message="Patch one document succeed.",
            data=data
        )
        return content

    def delete_one_by_id(self, id: UUID) -> Content[Document]:
        data: Document = document_repository.delete_one_by_id(id)
        content: Content[Document] = Content[Document](
            message="Delete one document succeed.",
            data=data
        )
        return content


document_manager = DocumentManager()
