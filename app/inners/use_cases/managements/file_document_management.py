from uuid import UUID

from sqlalchemy import exc
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from app.inners.models.daos.file_document import FileDocument
from app.inners.models.dtos.contracts.requests.managements.file_documents.create_one_body import CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.file_documents.patch_one_body import PatchOneBody
from app.inners.models.dtos.contracts.responses.managements.documents.file_document_response import FileDocumentResponse
from app.inners.models.dtos.contracts.result import Result
from app.inners.use_cases.managements.document_management import DocumentManagement
from app.outers.repositories.file_document_repository import FileDocumentRepository


class FileDocumentManagement:
    def __init__(
            self,
            document_management: DocumentManagement,
            file_document_repository: FileDocumentRepository,
    ):
        self.document_management: DocumentManagement = document_management
        self.file_document_repository: FileDocumentRepository = file_document_repository

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> Result[FileDocumentResponse]:
        try:
            found_file_document: FileDocument = await self.file_document_repository.find_one_by_id(
                session=session,
                id=id
            )
            result: Result[FileDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="FileDocumentManagement.find_one_by_id: Succeed.",
                data=found_file_document,
            )
        except exc.NoResultFound:
            result: Result[FileDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="FileDocumentManagement.find_one_by_id: Failed, file_document is not found.",
                data=None,
            )
        return result

    async def create_one(self, session: AsyncSession, body: CreateOneBody) -> Result[FileDocumentResponse]:
        file_document_to_create: FileDocument = FileDocument(**body.dict())
        created_file_document: FileDocument = await self.file_document_repository.create_one(
            session=session,
            file_document_to_create=file_document_to_create
        )
        result: Result[FileDocumentResponse] = Result(
            status_code=status.HTTP_201_CREATED,
            message="FileDocumentManagement.create_one: Succeed.",
            data=created_file_document,
        )
        return result

    async def create_one_raw(self, session: AsyncSession, file_document_to_create: FileDocument) -> Result[
        FileDocumentResponse]:
        created_file_document: FileDocument = await self.file_document_repository.create_one(
            session=session,
            file_document_to_create=file_document_to_create
        )
        result: Result[FileDocumentResponse] = Result(
            status_code=status.HTTP_201_CREATED,
            message="FileDocumentManagement.create_one_raw: Succeed.",
            data=created_file_document,
        )
        return result

    async def patch_one_by_id(self, session: AsyncSession, id: UUID, body: PatchOneBody) -> Result[
        FileDocumentResponse]:
        try:
            file_document_to_patch: FileDocument = FileDocument(**body.dict())
            patched_file_document: FileDocument = await self.file_document_repository.patch_one_by_id(
                session=session,
                id=id,
                file_document_to_patch=file_document_to_patch
            )
            result: Result[FileDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="FileDocumentManagement.patch_one_by_id: Succeed.",
                data=patched_file_document,
            )
        except exc.NoResultFound:
            result: Result[FileDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="FileDocumentManagement.patch_one_by_id: Failed, file_document is not found.",
                data=None,
            )
        return result

    async def patch_one_by_id_raw(self, session: AsyncSession, id: UUID, file_document_to_patch: FileDocument) -> \
            Result[
                FileDocumentResponse]:
        patched_file_document: FileDocument = await self.file_document_repository.patch_one_by_id(
            session=session,
            id=id,
            file_document_to_patch=file_document_to_patch
        )
        result: Result[FileDocumentResponse] = Result(
            status_code=status.HTTP_200_OK,
            message="FileDocumentManagement.patch_one_by_id_raw: Succeed.",
            data=patched_file_document,
        )
        return result

    async def delete_one_by_id(self, session: AsyncSession, id: UUID) -> Result[FileDocumentResponse]:
        try:
            deleted_file_document: FileDocument = await self.file_document_repository.delete_one_by_id(
                session=session,
                id=id
            )
            result: Result[FileDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="FileDocumentManagement.delete_one_by_id: Succeed.",
                data=deleted_file_document,
            )
        except exc.NoResultFound:
            result: Result[FileDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="FileDocumentManagement.delete_one_by_id: Failed, file_document is not found.",
                data=None,
            )
        return result
