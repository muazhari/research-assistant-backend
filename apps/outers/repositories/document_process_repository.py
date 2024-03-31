from uuid import UUID

import sqlalchemy
from sqlalchemy import exc
from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.document_process import DocumentProcess
from apps.outers.exceptions import repository_exception
from apps.outers.exceptions.base_exception import BaseException


class DocumentProcessRepository:

    def __init__(self):
        pass

    class NotFound(BaseException):
        pass

    class IntegrityError(BaseException):
        pass

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> DocumentProcess:
        try:
            found_document_process_result: Result = await session.execute(
                select(DocumentProcess).where(DocumentProcess.id == id).limit(1)
            )
            found_document_process: DocumentProcess = found_document_process_result.scalars().one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_document_process

    def create_one(self, session: AsyncSession, document_process_creator: DocumentProcess) -> DocumentProcess:
        try:
            session.add(document_process_creator)
        except sqlalchemy.exc.IntegrityError:
            raise repository_exception.IntegrityError()

        return document_process_creator

    async def patch_one_by_id(self, session: AsyncSession, id: UUID,
                              document_process_patcher: DocumentProcess) -> DocumentProcess:
        found_document_process: DocumentProcess = await self.find_one_by_id(
            session=session,
            id=id
        )
        found_document_process.patch_from(document_process_patcher.dict(exclude_none=True))
        return found_document_process

    async def delete_one_by_id(self, session: AsyncSession, id: UUID) -> DocumentProcess:
        found_document_process: DocumentProcess = await self.find_one_by_id(
            session=session,
            id=id
        )
        await session.delete(found_document_process)
        return found_document_process
