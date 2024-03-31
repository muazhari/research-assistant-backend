import io
from datetime import timedelta
from pathlib import Path
from uuid import UUID

import sqlalchemy
from minio.helpers import ObjectWriteResult
from sqlalchemy import exc
from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.file_document import FileDocument
from apps.outers.datastores.temp_datastore import TempDatastore
from apps.outers.datastores.three_datastore import ThreeDatastore
from apps.outers.exceptions import repository_exception
from apps.outers.exceptions.base_exception import BaseException


class FileDocumentRepository:

    def __init__(
            self,
            temp_datastore: TempDatastore,
            three_datastore: ThreeDatastore,

    ):
        self.temp_datastore: TempDatastore = temp_datastore
        self.three_datastore: ThreeDatastore = three_datastore
        self.file_path: Path = self.temp_datastore.temp_datastore_setting.TEMP_DATASTORE_PATH / "file_documents"
        self.file_path.mkdir(exist_ok=True)

    class NotFound(BaseException):
        pass

    class IntegrityError(BaseException):
        pass

    def save_file(self, file_name: str, file_data: bytes) -> Path:
        file_path: Path = self.file_path / file_name
        file_io = open(file_path, "wb")
        file_io.write(file_data)
        file_io.close()

        return file_path

    def read_file_data(self, file_name: str) -> bytes:
        file_path: Path = self.file_path / file_name
        file_io = open(file_path, "rb")
        file_data = file_io.read()
        file_io.close()

        return file_data

    def remove_file(self, file_name: str):
        file_path: Path = self.file_path / file_name
        file_path.unlink()

    def put_object(self, object_name: str, data: bytes) -> ObjectWriteResult:
        return self.three_datastore.client.put_object(
            bucket_name="research-assistant-backend.file-documents",
            object_name=object_name,
            data=io.BytesIO(data),
            length=len(data)
        )

    def remove_object(self, object_name: str):
        self.three_datastore.client.remove_object(
            bucket_name="research-assistant-backend.file-documents",
            object_name=object_name
        )

    def get_object_url(self, object_name: str) -> str:
        return self.three_datastore.client.get_presigned_url(
            bucket_name="research-assistant-backend.file-documents",
            object_name=object_name,
            method="GET",
            expires=timedelta(days=1)
        )

    def get_object_data(self, object_name: str) -> bytes:
        response = self.three_datastore.client.get_object(
            bucket_name="research-assistant-backend.file-documents",
            object_name=object_name,
        )
        file_data: bytes = response.read()
        response.close()

        return file_data

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> FileDocument:
        try:
            found_file_document_result: Result = await session.execute(
                select(FileDocument).where(FileDocument.id == id).limit(1)
            )
            found_file_document: FileDocument = found_file_document_result.scalars().one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_file_document

    def create_one(
            self,
            session: AsyncSession,
            file_document_creator: FileDocument,
            file_data: bytes
    ) -> FileDocument:
        try:
            session.add(file_document_creator)
            self.put_object(
                object_name=file_document_creator.file_name,
                data=file_data
            )
        except sqlalchemy.exc.IntegrityError:
            raise repository_exception.IntegrityError()

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
        self.put_object(
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
        self.remove_object(object_name=found_file_document.file_name)

        return found_file_document
