from uuid import UUID

from sqlmodel import select
from sqlmodel.sql import expression

from app.inner.model.entities.web_document import WebDocument
from app.outer.persistences.db import create_session


class WebDocumentRepository:
    def read_all(self) -> WebDocument:
        with create_session() as session:
            statement: expression = select(WebDocument)
            return session.exec(statement).all()

    def read_one_by_id(self, id: UUID) -> WebDocument:
        with create_session() as session:
            statement: expression = select(WebDocument).where(WebDocument.id == id)
            found_entity: WebDocument = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            return found_entity

    def create_one(self, entity: WebDocument) -> WebDocument:
        with create_session() as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def patch_one_by_id(self, id: UUID, entity: WebDocument) -> WebDocument:
        with create_session() as session:
            statement: expression = select(WebDocument).where(WebDocument.id == id)
            found_entity: WebDocument = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            found_entity.id = entity.id
            found_entity.document_id = entity.document_id
            found_entity.web_url = entity.web_url
            session.commit()
            session.refresh(found_entity)
            return found_entity

    def delete_one_by_id(self, id: UUID) -> WebDocument:
        with create_session() as session:
            statement: expression = select(WebDocument).where(WebDocument.id == id)
            found_entity: WebDocument = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            session.delete(found_entity)
            session.commit()
            return found_entity


web_document_repository = WebDocumentRepository()
