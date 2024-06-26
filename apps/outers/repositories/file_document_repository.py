import io
from datetime import timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
from uuid import UUID

import sqlalchemy
from minio.helpers import ObjectWriteResult
from sqlalchemy import exc
from sqlalchemy.engine import ScalarResult
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.exceptions import repository_exception
from apps.inners.models.daos.document import Document
from apps.inners.models.daos.file_document import FileDocument
from apps.outers.datastores.temp_datastore import TempDatastore
from apps.outers.datastores.three_datastore import ThreeDatastore


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

    def save_file(self, relative_file_path: Path, file_data: bytes) -> Path:
        relative_file_path: Path = self.file_path / relative_file_path
        file_io = open(relative_file_path, "wb")
        file_io.write(file_data)
        file_io.close()

        return relative_file_path

    def read_file_data(self, relative_file_path: Path) -> bytes:
        relative_file_path: Path = self.file_path / relative_file_path
        file_io = open(relative_file_path, "rb")
        file_data = file_io.read()
        file_io.close()

        return file_data

    def remove_file(self, relative_file_path: Path):
        relative_file_path: Path = self.file_path / relative_file_path
        relative_file_path.unlink()

    def put_object(self, object_name: str, data: bytes) -> ObjectWriteResult:
        return self.three_datastore.client.put_object(
            bucket_name="research-assistant-backend.file-documents",
            object_name=object_name,
            data=io.BytesIO(data),
            length=len(data)
        )

    def patch_object(self, old_object_name: str, new_object_name: str, new_data: bytes):
        self.remove_object(
            object_name=old_object_name
        )
        self.put_object(
            object_name=new_object_name,
            data=new_data
        )

    def remove_object(self, object_name: str):
        self.three_datastore.client.remove_object(
            bucket_name="research-assistant-backend.file-documents",
            object_name=object_name
        )

    def get_object_url(self, object_name: str, response_headers: Dict[str, Any] = None) -> str:
        return self.three_datastore.client.get_presigned_url(
            bucket_name="research-assistant-backend.file-documents",
            object_name=object_name,
            response_headers=response_headers,
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

    async def find_many_by_account_id_with_pagination(
            self,
            session: AsyncSession,
            account_id: UUID,
            page_position: int,
            page_size: int
    ) -> List[FileDocument]:
        found_file_document_result: ScalarResult = await session.exec(
            select(FileDocument)
            .join(Document, Document.id == FileDocument.id)
            .where(Document.account_id == account_id)
            .limit(page_size)
            .offset(page_size * (page_position - 1))
        )
        found_file_documents: List[FileDocument] = list(found_file_document_result.all())

        return found_file_documents

    async def find_one_by_id_and_account_id(self, session: AsyncSession, id: UUID, account_id: UUID) -> FileDocument:
        try:
            found_file_document_result: ScalarResult = await session.exec(
                select(FileDocument)
                .join(Document, Document.id == FileDocument.id)
                .where(FileDocument.id == id)
                .where(Document.account_id == account_id)
                .limit(1)
            )
            found_file_document: FileDocument = found_file_document_result.one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_file_document

    def create_one(
            self,
            session: AsyncSession,
            file_document_creator: FileDocument,
            file_data: Optional[bytes] = None
    ) -> FileDocument:
        try:
            session.add(file_document_creator)
            if file_data is not None:
                self.put_object(
                    object_name=file_document_creator.file_name,
                    data=file_data
                )
        except sqlalchemy.exc.IntegrityError:
            raise repository_exception.IntegrityError()

        return file_document_creator

    async def patch_one_by_id_and_account_id(
            self,
            session: AsyncSession,
            id: UUID,
            account_id: UUID,
            file_document_patcher: FileDocument,
            file_data: Optional[bytes] = None
    ) -> FileDocument:
        found_file_document: FileDocument = await self.find_one_by_id_and_account_id(
            session=session,
            id=id,
            account_id=account_id
        )
        found_file_document.patch_from(file_document_patcher.dict(exclude_none=True))
        if file_data is not None:
            self.patch_object(
                old_object_name=found_file_document.file_name,
                new_object_name=file_document_patcher.file_name,
                new_data=file_data
            )
        else:
            file_data = self.get_object_data(
                object_name=found_file_document.file_name
            )
            self.patch_object(
                old_object_name=found_file_document.file_name,
                new_object_name=file_document_patcher.file_name,
                new_data=file_data
            )

        return found_file_document

    async def delete_one_by_id_and_account_id(self, session: AsyncSession, id: UUID, account_id: UUID) -> FileDocument:
        found_file_document: FileDocument = await self.find_one_by_id_and_account_id(
            session=session,
            id=id,
            account_id=account_id
        )
        await session.delete(found_file_document)
        self.remove_object(object_name=found_file_document.file_name)

        return found_file_document
