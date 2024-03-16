from uuid import UUID

from sqlmodel import select
from sqlmodel.engine.result import Result
from sqlmodel.ext.asyncio.session import AsyncSession

from app.inners.models.daos.web_document import WebDocument


class WebDocumentRepository:

    def __init__(self):
        pass

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> WebDocument:
        found_web_document_result: Result = await session.execute(
            select(WebDocument).where(WebDocument.id == id).limit(1)
        )
        found_web_document: WebDocument = found_web_document_result.scalars().one()
        return found_web_document

    async def create_one(self, session: AsyncSession, web_document_to_create: WebDocument) -> WebDocument:
        session.add(web_document_to_create)
        return web_document_to_create

    async def patch_one_by_id(self, session: AsyncSession, id: UUID,
                              web_document_to_patch: WebDocument) -> WebDocument:
        found_web_document: WebDocument = await self.find_one_by_id(
            session=session,
            id=id
        )
        found_web_document.patch_from(web_document_to_patch.dict())
        return found_web_document

    async def delete_one_by_id(self, session: AsyncSession, id: UUID) -> WebDocument:
        found_web_document: WebDocument = await self.find_one_by_id(
            session=session,
            id=id
        )
        await session.delete(found_web_document)
        return found_web_document
