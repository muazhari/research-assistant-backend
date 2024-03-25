from sqlmodel import select
from sqlalchemy import Result
from sqlmodel.ext.asyncio.session import AsyncSession

from app.inners.models.daos.document_type import DocumentType


class DocumentTypeRepository:

    def __init__(self):
        pass

    async def find_one_by_id(self, session: AsyncSession, id: str) -> DocumentType:
        found_document_type_result: Result = await session.execute(
            select(DocumentType).where(DocumentType.id == id).limit(1)
        )
        found_document_type: DocumentType = found_document_type_result.scalars().one()
        return found_document_type

    async def create_one(self, session: AsyncSession, document_type_creator: DocumentType) -> DocumentType:
        session.add(document_type_creator)
        return document_type_creator

    async def patch_one_by_id(self, session: AsyncSession, id: str,
                              document_type_patcher: DocumentType) -> DocumentType:
        found_document_type: DocumentType = await self.find_one_by_id(
            session=session,
            id=id
        )
        found_document_type.patch_from(document_type_patcher.dict(exclude_none=True))
        return found_document_type

    async def delete_one_by_id(self, session: AsyncSession, id: str) -> DocumentType:
        found_document_type: DocumentType = await self.find_one_by_id(
            session=session,
            id=id
        )
        await session.delete(found_document_type)
        return found_document_type
