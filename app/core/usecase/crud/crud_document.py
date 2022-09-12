from uuid import UUID

from app.core.model.entity.document import Document
from app.infrastucture.repository import document_repository


def find_all() -> [Document]:
    documents: [Document] = document_repository.find_all()
    return documents


def find_one_by_id(id: UUID) -> Document:
    found_document: Document = document_repository.find_one_by_id(id)
    return found_document


def create_one(document: Document) -> Document:
    created_document = document_repository.create_one(document)
    return created_document


def update_one_by_id(id: UUID, document: Document) -> Document:
    found_document: Document = document_repository.update_one_by_id(id, document)
    return found_document


def delete_one_by_id(id: UUID, document: Document) -> Document:
    found_document: Document = document_repository.delete_one_by_id(id, document)
    return found_document
