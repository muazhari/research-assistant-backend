from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.web_document import WebDocument
from tests.fakes.web_document_fake import WebDocumentFake


class WebDocumentSeeder:

    def __init__(
            self,
            web_document_fake: WebDocumentFake
    ):
        self.web_document_fake: WebDocumentFake = web_document_fake

    async def up(self, session: AsyncSession):
        for web_document in self.web_document_fake.data:
            session.add(web_document)

    async def down(self, session: AsyncSession):
        for web_document in self.web_document_fake.data:
            found_web_document_result: Result = await session.execute(
                select(WebDocument).where(WebDocument.id == web_document.dict().get("id")).limit(1)
            )
            found_web_document: WebDocument = found_web_document_result.scalars().one()
            await session.delete(found_web_document)
