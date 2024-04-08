from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.document_process import DocumentProcess
from tests.fakes.document_process_fake import DocumentProcessFake


class DocumentProcessSeeder:

    def __init__(
            self,
            document_process_fake: DocumentProcessFake
    ):
        self.document_process_fake: DocumentProcessFake = document_process_fake

    async def up(self, session: AsyncSession):
        for document_process in self.document_process_fake.data:
            session.add(document_process)

    async def down(self, session: AsyncSession):
        for document_process in self.document_process_fake.data:
            found_document_process_result: Result = await session.execute(
                select(DocumentProcess).where(DocumentProcess.id == document_process.id).limit(1)
            )
            found_document_process: DocumentProcess = found_document_process_result.scalars().one()
            await session.delete(found_document_process)
