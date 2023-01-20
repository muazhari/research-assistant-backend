from uuid import UUID

from sqlmodel import select
from sqlmodel.sql import expression

from app.inner.model.entities.text_document import TextDocument
from app.outer.persistences.db import create_session


class TextDocumentRepository:
    def read_all(self) -> [TextDocument]:
        with create_session() as session:
            statement: expression = select(TextDocument)
            return session.exec(statement).all()

    def read_one_by_id(self, id: UUID) -> TextDocument:
        with create_session() as session:
            statement: expression = select(TextDocument).where(TextDocument.id == id)
            found_entity: TextDocument = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            return found_entity

    def read_one_by_document_id(self, document_id: UUID) -> TextDocument:
        with create_session() as session:
            statement: expression = select(TextDocument).where(TextDocument.document_id == document_id)
            found_entity: TextDocument = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            return found_entity

    def create_one(self, entity: TextDocument) -> TextDocument:
        with create_session() as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def patch_one_by_id(self, id: UUID, entity: TextDocument) -> TextDocument:
        with create_session() as session:
            statement: expression = select(TextDocument).where(TextDocument.id == id)
            found_entity: TextDocument = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            found_entity.id = entity.id
            found_entity.document_id = entity.document_id
            found_entity.text_content = entity.text_content
            session.commit()
            session.refresh(found_entity)
            return found_entity

    def delete_one_by_id(self, id: UUID) -> TextDocument:
        with create_session() as session:
            statement: expression = select(TextDocument).where(TextDocument.id == id)
            found_entity: TextDocument = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            session.delete(found_entity)
            session.commit()
            return found_entity


text_document_repository = TextDocumentRepository()
