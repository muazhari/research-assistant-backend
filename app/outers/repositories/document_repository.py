from typing import List
from uuid import UUID

from sqlmodel import select
from sqlmodel.sql import expression

from app.inners.models.entities.document import Document
from app.outers.persistences.datastore_one_persistence import DataStoreUtility


class DocumentRepository:

    def __init__(self):
        self.datastore_utility: DataStoreUtility = DataStoreUtility()

    async def read_all(self) -> List[Document]:
        async with await self.datastore_utility.create_session() as session:
            statement: expression = select(Document)
            result = await session.execute(statement)
            found_entities: List[Document] = result.scalars().all()
            return found_entities

    async def read_one_by_id(self, id: UUID) -> Document:
        async with await self.datastore_utility.create_session() as session:
            statement: expression = select(Document).where(Document.id == id)
            result = await session.execute(statement)
            found_entity: Document = result.scalars().one()
            if found_entity is None:
                raise Exception("Entity not found.")
            return found_entity

    async def create_one(self, entity: Document) -> Document:
        async with await self.datastore_utility.create_session() as session:
            try:
                session.add(entity)
                await session.commit()
                await session.refresh(entity)
            except Exception as exception:
                raise exception
        return entity

    async def patch_one_by_id(self, id: UUID, entity: Document) -> Document:
        async with await self.datastore_utility.create_session() as session:
            try:
                statement: expression = select(Document).where(Document.id == id)
                result = await session.execute(statement)
                found_entity: Document = result.scalars().one()
                if found_entity is None:
                    raise Exception("Entity not found.")
                found_entity.patch_from(entity.dict())
                await session.commit()
                await session.refresh(found_entity)
            except Exception as exception:
                raise exception
            return found_entity

    async def delete_one_by_id(self, id: UUID) -> Document:
        async with await self.datastore_utility.create_session() as session:
            try:
                statement: expression = select(Document).where(Document.id == id)
                result = await session.execute(statement)
                found_entity: Document = result.scalars().one()
                if found_entity is None:
                    raise Exception("Entity not found.")
                await session.delete(found_entity)
                await session.commit()
            except Exception as exception:
                raise exception
            return found_entity
