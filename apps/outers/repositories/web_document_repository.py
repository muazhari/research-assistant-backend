from typing import List
from uuid import UUID

import sqlalchemy
from sqlalchemy import exc
from sqlalchemy.engine import ScalarResult
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.exceptions import repository_exception
from apps.inners.models.daos.document import Document
from apps.inners.models.daos.web_document import WebDocument


class WebDocumentRepository:

    def __init__(self):
        pass

    async def find_many_by_account_id_with_pagination(
            self,
            session: AsyncSession,
            account_id: UUID,
            page_position: int,
            page_size: int
    ) -> List[WebDocument]:
        found_web_document_result: ScalarResult = await session.exec(
            select(WebDocument)
            .join(Document, Document.id == WebDocument.id)
            .where(Document.account_id == account_id)
            .limit(page_size)
            .offset(page_size * (page_position - 1))
        )
        found_web_documents: List[WebDocument] = list(found_web_document_result.all())

        return found_web_documents

    async def find_one_by_id_and_account_id(self, session: AsyncSession, id: UUID, account_id: UUID) -> WebDocument:
        try:
            found_web_document_result: ScalarResult = await session.exec(
                select(WebDocument)
                .join(Document, Document.id == WebDocument.id)
                .where(WebDocument.id == id)
                .where(Document.account_id == account_id)
            )
            found_web_document: WebDocument = found_web_document_result.one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_web_document

    def create_one(self, session: AsyncSession, web_document_creator: WebDocument) -> WebDocument:
        try:
            session.add(web_document_creator)
        except sqlalchemy.exc.IntegrityError:
            raise repository_exception.IntegrityError()

        return web_document_creator

    async def patch_one_by_id_and_account_id(
            self,
            session: AsyncSession,
            id: UUID,
            account_id: UUID,
            web_document_patcher: WebDocument
    ) -> WebDocument:
        found_web_document: WebDocument = await self.find_one_by_id_and_account_id(
            session=session,
            id=id,
            account_id=account_id
        )
        found_web_document.patch_from(web_document_patcher.dict(exclude_none=True))

        return found_web_document

    async def delete_one_by_id_and_account_id(self, session: AsyncSession, id: UUID, account_id: UUID) -> WebDocument:
        found_web_document: WebDocument = await self.find_one_by_id_and_account_id(
            session=session,
            id=id,
            account_id=account_id
        )
        await session.delete(found_web_document)

        return found_web_document
