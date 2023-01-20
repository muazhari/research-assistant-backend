from uuid import UUID

from sqlmodel import select
from sqlmodel.sql import expression

from app.inner.model.entities.document_process import DocumentProcess
from app.outer.persistences.db import create_session


class DocumentProcessRepository:
    def read_all(self) -> [DocumentProcess]:
        with create_session() as session:
            statement: expression = select(DocumentProcess)
            return session.exec(statement).all()

    def read_one_by_id(self, id: UUID) -> DocumentProcess:
        with create_session() as session:
            statement: expression = select(DocumentProcess).where(DocumentProcess.id == id)
            found_entity: DocumentProcess = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            return found_entity

    def create_one(self, entity: DocumentProcess) -> DocumentProcess:
        with create_session() as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def patch_one_by_id(self, id: UUID, entity: DocumentProcess) -> DocumentProcess:
        with create_session() as session:
            statement: expression = select(DocumentProcess).where(DocumentProcess.id == id)
            found_entity: DocumentProcess = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            found_entity.id = entity.id
            found_entity.initial_document_id = entity.initial_document_id
            found_entity.final_document_id = entity.final_document_id
            found_entity.process_duration = entity.process_duration
            found_entity.updated_at = entity.updated_at
            found_entity.created_at = entity.created_at
            session.commit()
            session.refresh(found_entity)
            return found_entity

    def delete_one_by_id(self, id: UUID) -> DocumentProcess:
        with create_session() as session:
            statement: expression = select(DocumentProcess).where(DocumentProcess.id == id)
            found_entity: DocumentProcess = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            session.delete(found_entity)
            session.commit()
            return found_entity


document_process_repository = DocumentProcessRepository()
