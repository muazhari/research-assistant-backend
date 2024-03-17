from sqlmodel import select
from sqlmodel.engine.result import Result
from sqlmodel.ext.asyncio.session import AsyncSession

from app.inners.models.daos.web_document import WebDocument
from test.mocks.web_document_mock import WebDocumentMock


class WebDocumentSeeder:

    def __init__(
            self,
            web_document_mock: WebDocumentMock
    ):
        self.web_document_mock: WebDocumentMock = web_document_mock

    async def up(self, session: AsyncSession):
        for web_document in self.web_document_mock.data:
            session.add(web_document)

    async def down(self, session: AsyncSession):

        for web_document in self.web_document_mock.data:
            found_web_document_result: Result = await session.execute(
                select(WebDocument).where(WebDocument.id == web_document.dict().get("id")).limit(1)
            )
            found_web_document: WebDocument = found_web_document_result.scalars().one()
            await session.delete(found_web_document)
