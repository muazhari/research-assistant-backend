from uuid import UUID

from sqlmodel import select
from sqlmodel.sql import expression

from app.inner.model.entities.document import Document
from app.outer.persistences.db import create_session


class DocumentRepository:
    def read_all(self) -> [Document]:
        with create_session() as session:
            statement: expression = select(Document)
            return session.exec(statement).all()

    def read_one_by_id(self, id: UUID) -> Document:
        with create_session() as session:
            statement: expression = select(Document).where(Document.id == id)
            found_entity: Document = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            return found_entity

    def create_one(self, entity: Document) -> Document:
        with create_session() as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def patch_one_by_id(self, id: UUID, entity: Document) -> Document:
        with create_session() as session:
            statement: expression = select(Document).where(Document.id == id)
            found_entity: Document = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            found_entity.id = entity.id
            found_entity.name = entity.name
            found_entity.description = entity.description
            found_entity.document_type_id = entity.document_type_id
            found_entity.account_id = entity.account_id
            found_entity.updated_at = entity.updated_at
            found_entity.created_at = entity.created_at
            session.commit()
            session.refresh(found_entity)
            return found_entity

    def delete_one_by_id(self, id: UUID) -> Document:
        with create_session() as session:
            statement: expression = select(Document).where(Document.id == id)
            found_entity: Document = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            session.delete(found_entity)
            session.commit()
            return found_entity


document_repository = DocumentRepository()
