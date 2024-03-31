from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.text_document import TextDocument
from tests.mocks.text_document_mock import TextDocumentMock


class TextDocumentSeeder:

    def __init__(
            self,
            text_document_mock: TextDocumentMock
    ):
        self.text_document_mock: TextDocumentMock = text_document_mock

    async def up(self, session: AsyncSession):
        for text_document in self.text_document_mock.data:
            session.add(text_document)

    async def down(self, session: AsyncSession):
        for text_document in self.text_document_mock.data:
            found_text_document_result: Result = await session.execute(
                select(TextDocument).where(TextDocument.id == text_document.id).limit(1)
            )
            found_text_document: TextDocument = found_text_document_result.scalars().one()
            await session.delete(found_text_document)
