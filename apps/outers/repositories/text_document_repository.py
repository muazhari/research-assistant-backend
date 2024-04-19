from typing import List
from uuid import UUID

import sqlalchemy
from sqlalchemy import exc
from sqlalchemy.engine import ScalarResult
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.exceptions import repository_exception
from apps.inners.models.daos.document import Document
from apps.inners.models.daos.text_document import TextDocument


class TextDocumentRepository:

    def __init__(self):
        pass

    async def find_many_by_account_id_with_pagination(
            self,
            session: AsyncSession,
            account_id: UUID,
            page_position: int,
            page_size: int
    ) -> List[TextDocument]:
        found_text_document_result: ScalarResult = await session.exec(
            select(TextDocument)
            .join(Document, Document.id == TextDocument.id)
            .where(Document.account_id == account_id)
            .limit(page_size)
            .offset(page_size * (page_position - 1))
        )
        found_text_documents: List[TextDocument] = list(found_text_document_result.all())

        return found_text_documents

    async def find_one_by_id_and_account_id(self, session: AsyncSession, id: UUID, account_id: UUID) -> TextDocument:
        try:
            found_text_document_result: ScalarResult = await session.exec(
                select(TextDocument)
                .join(Document, Document.id == TextDocument.id)
                .where(TextDocument.id == id)
                .where(Document.account_id == account_id)
            )
            found_text_document: TextDocument = found_text_document_result.one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_text_document

    def create_one(self, session: AsyncSession, text_document_creator: TextDocument) -> TextDocument:
        try:
            session.add(text_document_creator)
        except sqlalchemy.exc.IntegrityError:
            raise repository_exception.IntegrityError()

        return text_document_creator

    async def patch_one_by_id_and_account_id(
            self,
            session: AsyncSession,
            id: UUID,
            account_id: UUID,
            text_document_patcher: TextDocument
    ) -> TextDocument:
        found_text_document: TextDocument = await self.find_one_by_id_and_account_id(
            session=session,
            id=id,
            account_id=account_id
        )
        found_text_document.patch_from(text_document_patcher.dict(exclude_none=True))

        return found_text_document

    async def delete_one_by_id_and_account_id(self, session: AsyncSession, id: UUID, account_id: UUID) -> TextDocument:
        found_text_document: TextDocument = await self.find_one_by_id_and_account_id(
            session=session,
            id=id,
            account_id=account_id
        )
        await session.delete(found_text_document)

        return found_text_document
