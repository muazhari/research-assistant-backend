from uuid import UUID

import sqlalchemy
from sqlalchemy import exc
from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.text_document import TextDocument
from apps.outers.exceptions import repository_exception
from apps.outers.exceptions.base_exception import BaseException


class TextDocumentRepository:

    def __init__(self):
        pass

    class NotFound(BaseException):
        pass

    class IntegrityError(BaseException):
        pass

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> TextDocument:
        try:
            found_text_document_result: Result = await session.execute(
                select(TextDocument).where(TextDocument.id == id).limit(1)
            )
            found_text_document: TextDocument = found_text_document_result.scalars().one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_text_document

    def create_one(self, session: AsyncSession, text_document_creator: TextDocument) -> TextDocument:
        try:
            session.add(text_document_creator)
        except sqlalchemy.exc.IntegrityError:
            raise repository_exception.IntegrityError()

        return text_document_creator

    async def patch_one_by_id(self, session: AsyncSession, id: UUID,
                              text_document_patcher: TextDocument) -> TextDocument:
        found_text_document: TextDocument = await self.find_one_by_id(
            session=session,
            id=id
        )
        found_text_document.patch_from(text_document_patcher.dict(exclude_none=True))

        return found_text_document

    async def delete_one_by_id(self, session: AsyncSession, id: UUID) -> TextDocument:
        found_text_document: TextDocument = await self.find_one_by_id(
            session=session,
            id=id
        )
        await session.delete(found_text_document)

        return found_text_document
