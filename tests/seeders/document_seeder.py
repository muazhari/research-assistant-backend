from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.document import Document
from tests.fakes.document_fake import DocumentFake


class DocumentSeeder:

    def __init__(
            self,
            document_fake: DocumentFake
    ):
        self.document_fake: DocumentFake = document_fake

    async def up(self, session: AsyncSession):
        for document in self.document_fake.data:
            session.add(document)

    async def down(self, session: AsyncSession):
        for document in self.document_fake.data:
            found_document_result: Result = await session.exec(
                select(Document).where(Document.id == document.id).limit(1)
            )
            found_document: Document = found_document_result.one()
            await session.delete(found_document)
