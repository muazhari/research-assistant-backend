import datetime
import uuid
from typing import List
from uuid import UUID

from app.inner.model.entities.web_document import WebDocument
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.web_document.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.web_document.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content
from app.outer.repositories.web_document_repository import web_document_repository


class WebDocumentManager:
    def read_all(self) -> Content[List[WebDocument]]:
        data: WebDocument = web_document_repository.read_all()
        content: Content[List[WebDocument]] = Content[List[WebDocument]](
            message="Read all web_document succeed.",
            data=data
        )
        return content

    def read_one_by_id(self, id: UUID) -> Content[WebDocument]:
        data: WebDocument = web_document_repository.read_one_by_id(id)
        content: Content[WebDocument] = Content[WebDocument](
            message="Read one web_document succeed.",
            data=data
        )
        return content

    def read_one_by_document_id(self, document_id: UUID) -> Content[WebDocument]:
        data: WebDocument = web_document_repository.read_one_by_document_id(document_id)
        content: Content[WebDocument] = Content[WebDocument](
            message="Read one web_document by document_id succeed.",
            data=data
        )
        return content

    def create_one(self, entity_request: CreateOneRequest) -> Content[WebDocument]:
        entity: WebDocument = WebDocument(
            id=uuid.uuid4(),
            document_id=entity_request.document_id,
            web_url=entity_request.web_url,
        )

        data: WebDocument = web_document_repository.create_one(entity)
        content: Content[WebDocument] = Content[WebDocument](
            message="Create one web_document succeed.",
            data=data
        )
        return content

    def patch_one_by_id(self, id: UUID, entity_request: PatchOneByIdRequest) -> Content[WebDocument]:
        found_entity: WebDocument = web_document_repository.read_one_by_id(id)

        entity: WebDocument = WebDocument(
            id=found_entity.id,
            document_id=entity_request.document_id,
            web_url=entity_request.web_url,
        )

        data: WebDocument = web_document_repository.patch_one_by_id(id, entity)
        content: Content[WebDocument] = Content[WebDocument](
            message="Patch one web_document by id succeed.",
            data=data
        )
        return content

    def delete_one_by_id(self, id: UUID) -> Content[WebDocument]:
        data: WebDocument = web_document_repository.delete_one_by_id(id)
        content: Content[WebDocument] = Content[WebDocument](
            message="Delete one web_document by id succeed.",
            data=data
        )
        return content


web_document_manager = WebDocumentManager()
