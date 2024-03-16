from uuid import UUID

from sqlmodel import select
from sqlmodel.engine.result import Result
from sqlmodel.ext.asyncio.session import AsyncSession

from app.inners.models.daos.document_process import DocumentProcess


class DocumentProcessRepository:

    def __init__(self):
        pass

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> DocumentProcess:
        found_document_process_result: Result = await session.execute(
            select(DocumentProcess).where(DocumentProcess.id == id).limit(1)
        )
        found_document_process: DocumentProcess = found_document_process_result.scalars().one()
        return found_document_process

    async def create_one(self, session: AsyncSession, document_process_to_create: DocumentProcess) -> DocumentProcess:
        session.add(document_process_to_create)
        return document_process_to_create

    async def patch_one_by_id(self, session: AsyncSession, id: UUID,
                              document_process_to_patch: DocumentProcess) -> DocumentProcess:
        found_document_process: DocumentProcess = await self.find_one_by_id(
            session=session,
            id=id
        )
        found_document_process.patch_from(document_process_to_patch.dict())
        return found_document_process

    async def delete_one_by_id(self, session: AsyncSession, id: UUID) -> DocumentProcess:
        found_document_process: DocumentProcess = await self.find_one_by_id(
            session=session,
            id=id
        )
        await session.delete(found_document_process)
        return found_document_process
