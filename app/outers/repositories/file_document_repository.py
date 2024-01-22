from typing import List
from uuid import UUID

from sqlmodel import select
from sqlmodel.sql import expression

from app.inners.models.entities.file_document import FileDocument
from app.outers.datastores.one_datastore import OneDatastore


class FileDocumentRepository:

    def __init__(self, one_datastore: OneDatastore):
        self.one_datastore: OneDatastore = one_datastore

    async def read_all(self) -> List[FileDocument]:
        async with await self.one_datastore.create_session() as session:
            statement: expression = select(FileDocument)
            result = await session.execute(statement)
            found_entities: List[FileDocument] = result.scalars().all()
            return found_entities

    async def read_one_by_id(self, id: UUID) -> FileDocument:
        async with await self.one_datastore.create_session() as session:
            statement: expression = select(FileDocument).where(FileDocument.id == id)
            result = await session.execute(statement)
            found_entity: FileDocument = result.scalars().one()
            if found_entity is None:
                raise Exception("Entity not found.")
            return found_entity

    async def read_one_by_document_id(self, document_id: UUID) -> FileDocument:
        async with await self.one_datastore.create_session() as session:
            statement: expression = select(FileDocument).where(FileDocument.document_id == document_id)
            result = await session.execute(statement)
            found_entity: FileDocument = result.scalars().one()
            if found_entity is None:
                raise Exception("Entity not found.")
            return found_entity

    async def create_one(self, entity: FileDocument) -> FileDocument:
        async with await self.one_datastore.create_session() as session:
            try:
                session.add(entity)
                await session.commit()
                await session.refresh(entity)
            except Exception as exception:
                raise exception
        return entity

    async def patch_one_by_id(self, id: UUID, entity: FileDocument) -> FileDocument:
        async with await self.one_datastore.create_session() as session:
            try:
                statement: expression = select(FileDocument).where(FileDocument.id == id)
                result = await session.execute(statement)
                found_entity: FileDocument = result.scalars().one()
                if found_entity is None:
                    raise Exception("Entity not found.")
                found_entity.patch_from(entity.dict())
                await session.commit()
                await session.refresh(found_entity)
            except Exception as exception:
                raise exception
            return found_entity

    async def delete_one_by_id(self, id: UUID) -> FileDocument:
        async with await self.one_datastore.create_session() as session:
            try:
                statement: expression = select(FileDocument).where(FileDocument.id == id)
                result = await session.execute(statement)
                found_entity: FileDocument = result.scalars().one()
                if found_entity is None:
                    raise Exception("Entity not found.")
                await session.delete(found_entity)
                await session.commit()
            except Exception as exception:
                raise exception
            return found_entity

    async def delete_one_by_document_id(self, document_id: UUID) -> FileDocument:
        async with await self.one_datastore.create_session() as session:
            try:
                statement: expression = select(FileDocument).where(FileDocument.document_id == document_id)
                result = await session.execute(statement)
                found_entity: FileDocument = result.scalars().one()
                if found_entity is None:
                    raise Exception("Entity not found.")
                await session.delete(found_entity)
                await session.commit()
            except Exception as exception:
                raise exception
            return found_entity
