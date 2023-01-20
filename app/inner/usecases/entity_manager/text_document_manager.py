import datetime
import uuid
from typing import List
from uuid import UUID

from app.inner.model.entities.text_document import TextDocument
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.text_document.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.text_document.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content
from app.outer.repositories.text_document_repository import text_document_repository


class TextDocumentManager:
    def read_all(self) -> Content[List[TextDocument]]:
        data: TextDocument = text_document_repository.read_all()
        content: Content[List[TextDocument]] = Content[List[TextDocument]](
            message="Read all text_document succeed.",
            data=data
        )
        return content

    def read_one_by_id(self, id: UUID) -> Content[TextDocument]:
        data: TextDocument = text_document_repository.read_one_by_id(id)
        content: Content[TextDocument] = Content[TextDocument](
            message="Read one text_document by id succeed.",
            data=data
        )
        return content

    def read_one_by_document_id(self, document_id: UUID) -> Content[TextDocument]:
        data: TextDocument = text_document_repository.read_one_by_document_id(document_id)
        content: Content[TextDocument] = Content[TextDocument](
            message="Read one text_document by document_id succeed.",
            data=data
        )
        return content

    def create_one(self, entity_request: CreateOneRequest) -> Content[TextDocument]:
        entity: TextDocument = TextDocument(
            id=uuid.uuid4(),
            document_id=entity_request.document_id,
            text_content=entity_request.text_content,
        )

        data: TextDocument = text_document_repository.create_one(entity)
        content: Content[TextDocument] = Content[TextDocument](
            message="Create one text_document succeed.",
            data=data
        )
        return content

    def patch_one_by_id(self, id: UUID, entity_request: PatchOneByIdRequest) -> Content[TextDocument]:
        found_entity: TextDocument = text_document_repository.read_one_by_id(id)

        entity: TextDocument = TextDocument(
            id=found_entity.id,
            document_id=entity_request.document_id,
            text_content=entity_request.text_content
        )

        data: TextDocument = text_document_repository.patch_one_by_id(id, entity)
        content: Content[TextDocument] = Content[TextDocument](
            message="Patch one text_document succeed.",
            data=data
        )
        return content

    def delete_one_by_id(self, id: UUID) -> Content[TextDocument]:
        data: TextDocument = text_document_repository.delete_one_by_id(id)
        content: Content[TextDocument] = Content[TextDocument](
            message="Delete one text_document succeed.",
            data=data
        )
        return content


text_document_manager = TextDocumentManager()
