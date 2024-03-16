from sqlmodel import select
from sqlmodel.engine.result import Result
from sqlmodel.ext.asyncio.session import AsyncSession

from app.inners.models.daos.document_process import DocumentProcess
from test.mocks.document_process_mock import DocumentProcessMock


class DocumentProcessSeeder:

    def __init__(
            self,
            document_process_mock: DocumentProcessMock
    ):
        self.document_process_mock: DocumentProcessMock = document_process_mock

    async def up(self, session: AsyncSession):
        for document_process in self.document_process_mock.data:
            session.add(document_process)

    async def down(self, session: AsyncSession):
        for document_process in self.document_process_mock.data:
            found_document_process_result: Result = await session.execute(
                select(DocumentProcess).where(DocumentProcess.id == document_process.id).limit(1)
            )
            found_document_process: DocumentProcess = found_document_process_result.scalars().one()
            await session.delete(found_document_process)
