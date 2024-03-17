from uuid import UUID

from sqlmodel import select
from sqlmodel.engine.result import Result
from sqlmodel.ext.asyncio.session import AsyncSession

from app.inners.models.daos.document import Document


class DocumentRepository:

    def __init__(self):
        pass

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> Document:
        found_document_result: Result = await session.execute(
            select(Document).where(Document.id == id).limit(1)
        )
        found_document: Document = found_document_result.scalars().one()
        return found_document

    async def create_one(self, session: AsyncSession, document_to_create: Document) -> Document:
        session.add(document_to_create)
        return document_to_create

    async def patch_one_by_id(self, session: AsyncSession, id: UUID,
                              document_to_patch: Document) -> Document:
        found_document: Document = await self.find_one_by_id(
            session=session,
            id=id
        )
        found_document.patch_from(document_to_patch.dict(exclude_none=True))
        return found_document

    async def delete_one_by_id(self, session: AsyncSession, id: UUID) -> Document:
        found_document: Document = await self.find_one_by_id(
            session=session,
            id=id
        )
        await session.delete(found_document)
        return found_document
