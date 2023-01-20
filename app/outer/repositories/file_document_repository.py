from uuid import UUID

from sqlmodel import select
from sqlmodel.sql import expression

from app.inner.model.entities.file_document import FileDocument
from app.outer.persistences.db import create_session


class FileDocumentRepository:
    def read_all(self) -> [FileDocument]:
        with create_session() as session:
            statement: expression = select(FileDocument)
            return session.exec(statement).all()

    def read_one_by_id(self, id: UUID) -> FileDocument:
        with create_session() as session:
            statement: expression = select(FileDocument).where(FileDocument.id == id)
            found_entity: FileDocument = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            return found_entity

    def read_one_by_document_id(self, document_id: UUID) -> FileDocument:
        with create_session() as session:
            statement: expression = select(FileDocument).where(FileDocument.document_id == document_id)
            found_entity: FileDocument = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            return found_entity

    def create_one(self, entity: FileDocument) -> FileDocument:
        with create_session() as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def patch_one_by_id(self, id: UUID, entity: FileDocument) -> FileDocument:
        with create_session() as session:
            statement: expression = select(FileDocument).where(FileDocument.id == id)
            found_entity: FileDocument = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            found_entity.id = entity.id
            found_entity.document_id = entity.document_id
            found_entity.file_name = entity.file_name
            found_entity.file_extension = entity.file_extension
            found_entity.file_bytes = entity.file_bytes
            session.commit()
            session.refresh(found_entity)
            return found_entity

    def delete_one_by_id(self, id: UUID) -> FileDocument:
        with create_session() as session:
            statement: expression = select(FileDocument).where(FileDocument.id == id)
            found_entity: FileDocument = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            session.delete(found_entity)
            session.commit()
            return found_entity


file_document_repository = FileDocumentRepository()
