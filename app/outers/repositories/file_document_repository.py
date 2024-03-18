from uuid import UUID

from sqlmodel import select
from sqlmodel.engine.result import Result
from sqlmodel.ext.asyncio.session import AsyncSession

from app.inners.models.daos.file_document import FileDocument


class FileDocumentRepository:

    def __init__(self):
        pass

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> FileDocument:
        found_file_document_result: Result = await session.execute(
            select(FileDocument).where(FileDocument.id == id).limit(1)
        )
        found_file_document: FileDocument = found_file_document_result.scalars().one()
        return found_file_document

    async def create_one(self, session: AsyncSession, file_document_creator: FileDocument) -> FileDocument:
        session.add(file_document_creator)
        return file_document_creator

    async def patch_one_by_id(self, session: AsyncSession, id: UUID,
                              file_document_patcher: FileDocument) -> FileDocument:
        found_file_document: FileDocument = await self.find_one_by_id(
            session=session,
            id=id
        )
        found_file_document.patch_from(file_document_patcher.dict(exclude_none=True))
        return found_file_document

    async def delete_one_by_id(self, session: AsyncSession, id: UUID) -> FileDocument:
        found_file_document: FileDocument = await self.find_one_by_id(
            session=session,
            id=id
        )
        await session.delete(found_file_document)
        return found_file_document
