from typing import List
from uuid import UUID

import sqlalchemy
from sqlalchemy import exc
from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.exceptions import repository_exception
from apps.inners.models.daos.document import Document


class DocumentRepository:

    def __init__(self):
        pass

    async def find_many_by_account_id_with_pagination(
            self,
            session: AsyncSession,
            account_id: UUID,
            page_number: int,
            page_size: int
    ) -> List[Document]:
        try:
            found_document_result: Result = await session.execute(
                select(Document)
                .where(Document.account_id == account_id)
                .limit(page_size)
                .offset(page_size * (page_number - 1))
            )
            found_documents: List[Document] = found_document_result.scalars().all()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_documents

    async def find_many_by_id_and_account_id(
            self,
            session: AsyncSession,
            ids: List[UUID],
            account_id: UUID,
    ) -> List[Document]:
        try:
            found_document_result: Result = await session.execute(
                select(Document)
                .where(Document.account_id == account_id)
                .where(Document.id.in_(ids))
                .limit(len(ids))
            )
            found_documents: List[Document] = found_document_result.scalars().all()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_documents

    async def find_one_by_id_and_accound_id(self, session: AsyncSession, id: UUID, account_id: UUID) -> Document:
        try:
            found_document_result: Result = await session.execute(
                select(Document)
                .where(Document.id == id)
                .where(Document.account_id == account_id)
                .limit(1)
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

    async def patch_one_by_id_and_account_id(self, session: AsyncSession, id: UUID, account_id: UUID,
                                             document_patcher: Document) -> Document:
        found_document: Document = await self.find_one_by_id_and_accound_id(
            session=session,
            id=id,
            account_id=account_id
        )
        found_document.patch_from(document_patcher.dict(exclude_none=True))
        return found_document

    async def delete_one_by_id_and_account_id(self, session: AsyncSession, id: UUID, account_id: UUID) -> Document:
        found_document: Document = await self.find_one_by_id_and_accound_id(
            session=session,
            id=id,
            account_id=account_id
        )
        await session.delete(found_document)
        return found_document
