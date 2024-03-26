from sqlmodel import select
from sqlalchemy.engine import Result
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.document import Document
from tests.mocks.document_mock import DocumentMock


class DocumentSeeder:

    def __init__(
            self,
            document_mock: DocumentMock
    ):
        self.document_mock: DocumentMock = document_mock

    async def up(self, session: AsyncSession):
        for document in self.document_mock.data:
            session.add(document)

    async def down(self, session: AsyncSession):
        for document in self.document_mock.data:
            found_document_result: Result = await session.execute(
                select(Document).where(Document.id == document.id).limit(1)
            )
            found_document: Document = found_document_result.scalars().one()
            await session.delete(found_document)
