from uuid import UUID

import sqlalchemy
from sqlalchemy import exc
from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.document import Document
from apps.outers.exceptions import repository_exception
from apps.outers.exceptions.base_exception import BaseException


class DocumentRepository:

    def __init__(self):
        pass

    class NotFound(BaseException):
        pass

    class IntegrityError(BaseException):
        pass

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> Document:
        try:
            found_document_result: Result = await session.execute(
                select(Document).where(Document.id == id).limit(1)
            )
            found_document: Document = found_document_result.scalars().one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_document

    def create_one(self, session: AsyncSession, document_creator: Document) -> Document:
        try:
            session.add(document_creator)
        except sqlalchemy.exc.IntegrityError:
            raise repository_exception.IntegrityError()

        return document_creator

    async def patch_one_by_id(self, session: AsyncSession, id: UUID, document_patcher: Document) -> Document:
        found_document: Document = await self.find_one_by_id(
            session=session,
            id=id
        )
        found_document.patch_from(document_patcher.dict(exclude_none=True))
        return found_document

    async def delete_one_by_id(self, session: AsyncSession, id: UUID) -> Document:
        found_document: Document = await self.find_one_by_id(
            session=session,
            id=id
        )
        await session.delete(found_document)
        return found_document
