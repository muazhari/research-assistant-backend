from uuid import UUID

import sqlalchemy
from sqlalchemy import exc
from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.web_document import WebDocument
from apps.outers.exceptions import repository_exception
from apps.outers.exceptions.base_exception import BaseException


class WebDocumentRepository:

    def __init__(self):
        pass

    class NotFound(BaseException):
        pass

    class IntegrityError(BaseException):
        pass

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> WebDocument:
        try:
            found_web_document_result: Result = await session.execute(
                select(WebDocument).where(WebDocument.id == id).limit(1)
            )
            found_web_document: WebDocument = found_web_document_result.scalars().one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_web_document

    def create_one(self, session: AsyncSession, web_document_creator: WebDocument) -> WebDocument:
        try:
            session.add(web_document_creator)
        except sqlalchemy.exc.IntegrityError:
            raise repository_exception.IntegrityError()

        return web_document_creator

    async def patch_one_by_id(self, session: AsyncSession, id: UUID,
                              web_document_patcher: WebDocument) -> WebDocument:
        found_web_document: WebDocument = await self.find_one_by_id(
            session=session,
            id=id
        )
        found_web_document.patch_from(web_document_patcher.dict(exclude_none=True))

        return found_web_document

    async def delete_one_by_id(self, session: AsyncSession, id: UUID) -> WebDocument:
        found_web_document: WebDocument = await self.find_one_by_id(
            session=session,
            id=id
        )
        await session.delete(found_web_document)

        return found_web_document
