from typing import List
from uuid import UUID

import sqlalchemy
from sqlalchemy import exc
from sqlalchemy.engine import ScalarResult
from sqlalchemy.orm import aliased
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.exceptions import repository_exception
from apps.inners.models.daos.document import Document
from apps.inners.models.daos.document_process import DocumentProcess


class DocumentProcessRepository:

    def __init__(self):
        pass

    async def find_many_by_account_id_with_pagination(
            self,
            session: AsyncSession,
            account_id: UUID,
            page_position: int,
            page_size: int
    ) -> List[DocumentProcess]:
        initial_document: Document = aliased(Document)
        final_document: Document = aliased(Document)
        found_document_process_result: ScalarResult = await session.exec(
            select(DocumentProcess)
            .join(initial_document, initial_document.id == DocumentProcess.initial_document_id)
            .join(final_document, final_document.id == DocumentProcess.final_document_id)
            .where(initial_document.account_id == account_id)
            .where(final_document.account_id == account_id)
            .limit(page_size)
            .offset(page_size * (page_position - 1))
        )
        found_document_processes: List[DocumentProcess] = list(found_document_process_result.all())

        return found_document_processes

    async def find_one_by_id_and_accound_id(self, session: AsyncSession, id: UUID, account_id: UUID) -> DocumentProcess:
        try:
            initial_document: Document = aliased(Document)
            final_document: Document = aliased(Document)
            found_document_process_result: ScalarResult = await session.exec(
                select(DocumentProcess)
                .join(initial_document, initial_document.id == DocumentProcess.initial_document_id)
                .join(final_document, final_document.id == DocumentProcess.final_document_id)
                .where(DocumentProcess.id == id)
                .where(initial_document.account_id == account_id)
                .where(final_document.account_id == account_id)
                .limit(1)
            )
            found_document_process: DocumentProcess = found_document_process_result.one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_document_process

    def create_one(self, session: AsyncSession, document_process_creator: DocumentProcess) -> DocumentProcess:
        try:
            session.add(document_process_creator)
        except sqlalchemy.exc.IntegrityError:
            raise repository_exception.IntegrityError()

        return document_process_creator

    async def patch_one_by_id_and_account_id(self, session: AsyncSession, id: UUID, account_id: UUID,
                                             document_process_patcher: DocumentProcess) -> DocumentProcess:
        found_document_process: DocumentProcess = await self.find_one_by_id_and_accound_id(
            session=session,
            id=id,
            account_id=account_id
        )
        found_document_process.patch_from(document_process_patcher.dict(exclude_none=True))
        return found_document_process

    async def delete_one_by_id_and_account_id(self, session: AsyncSession, id: UUID,
                                              account_id: UUID) -> DocumentProcess:
        found_document_process: DocumentProcess = await self.find_one_by_id_and_accound_id(
            session=session,
            id=id,
            account_id=account_id
        )
        await session.delete(found_document_process)
        return found_document_process
