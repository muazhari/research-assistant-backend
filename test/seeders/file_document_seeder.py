from sqlmodel import select
from sqlmodel.engine.result import Result
from sqlmodel.ext.asyncio.session import AsyncSession

from app.inners.models.daos.file_document import FileDocument
from test.mocks.file_document_mock import FileDocumentMock


class FileDocumentSeeder:

    def __init__(
            self,
            file_document_mock: FileDocumentMock
    ):
        self.file_document_mock: FileDocumentMock = file_document_mock

    async def up(self, session: AsyncSession):
        for file_document in self.file_document_mock.data:
            session.add(file_document)

    async def down(self, session: AsyncSession):
        for file_document in self.file_document_mock.data:
            found_file_document_result: Result = await session.execute(
                select(FileDocument).where(FileDocument.id == file_document.id).limit(1)
            )
            found_file_document: FileDocument = found_file_document_result.scalars().one()
            await session.delete(found_file_document)
