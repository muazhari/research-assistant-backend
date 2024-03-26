import io
from uuid import UUID

from sqlalchemy import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.inners.models.daos.file_document import FileDocument
from app.outers.datastores.three_datastore import ThreeDatastore


class FileDocumentRepository:

    def __init__(
            self,
            three_datastore: ThreeDatastore
    ):
        self.three_datastore: ThreeDatastore = three_datastore

    async def put_object(self, object_name: str, data: bytes):
        await self.three_datastore.client.put_object(
            bucket_name="research-assistant-backend.file-documents",
            object_name=object_name,
            data=io.BytesIO(data),
            length=len(data)
        )

    async def remove_object(self, object_name: str):
        await self.three_datastore.client.remove_object(
            bucket_name="research-assistant-backend.file-documents",
            object_name=object_name
        )

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> FileDocument:
        found_file_document_result: Result = await session.execute(
            select(FileDocument).where(FileDocument.id == id).limit(1)
        )
        found_file_document: FileDocument = found_file_document_result.scalars().one()
        return found_file_document

    async def create_one(
            self,
            session: AsyncSession,
            file_document_creator: FileDocument,
            file_data: bytes
    ) -> FileDocument:
        session.add(file_document_creator)
        await self.put_object(
            object_name=file_document_creator.file_name,
            data=file_data
        )
        return file_document_creator

    async def patch_one_by_id(
            self,
            session: AsyncSession,
            id: UUID,
            file_document_patcher: FileDocument,
            file_data: bytes
    ) -> FileDocument:
        found_file_document: FileDocument = await self.find_one_by_id(
            session=session,
            id=id
        )
        found_file_document.patch_from(file_document_patcher.dict(exclude_none=True))
        await self.put_object(
            object_name=found_file_document.file_name,
            data=file_data
        )
        return found_file_document

    async def delete_one_by_id(self, session: AsyncSession, id: UUID) -> FileDocument:
        found_file_document: FileDocument = await self.find_one_by_id(
            session=session,
            id=id
        )
        await session.delete(found_file_document)
        await self.remove_object(object_name=found_file_document.file_name)
        return found_file_document
