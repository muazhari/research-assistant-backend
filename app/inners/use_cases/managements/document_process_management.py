from uuid import UUID

from sqlalchemy import exc
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from app.inners.models.daos.document_process import DocumentProcess
from app.inners.models.dtos.contracts.requests.managements.document_processes.create_one_body import CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.document_processes.patch_one_body import PatchOneBody
from app.inners.models.dtos.contracts.result import Result
from app.outers.repositories.document_process_repository import DocumentProcessRepository


class DocumentProcessManagement:
    def __init__(
            self,
            document_process_repository: DocumentProcessRepository,
    ):
        self.document_process_repository: DocumentProcessRepository = document_process_repository

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> Result[DocumentProcess]:
        try:
            found_document_process: DocumentProcess = await self.document_process_repository.find_one_by_id(
                session=session,
                id=id
            )
            result: Result[DocumentProcess] = Result(
                status_code=status.HTTP_200_OK,
                message="DocumentProcessManagement.find_one_by_id: Succeed.",
                data=found_document_process,
            )
        except exc.NoResultFound:
            result: Result[DocumentProcess] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="DocumentProcessManagement.find_one_by_id: Failed, document_process is not found.",
                data=None,
            )
        return result

    async def create_one(self, session: AsyncSession, body: CreateOneBody) -> Result[DocumentProcess]:
        document_process_to_create: DocumentProcess = DocumentProcess(**body.dict())
        created_document_process: DocumentProcess = await self.document_process_repository.create_one(
            session=session,
            document_process_to_create=document_process_to_create
        )
        result: Result[DocumentProcess] = Result(
            status_code=status.HTTP_201_CREATED,
            message="DocumentProcessManagement.create_one: Succeed.",
            data=created_document_process,
        )
        return result

    async def create_one_raw(self, session: AsyncSession, document_process_to_create: DocumentProcess) -> Result[
        DocumentProcess]:
        created_document_process: DocumentProcess = await self.document_process_repository.create_one(
            session=session,
            document_process_to_create=document_process_to_create
        )
        result: Result[DocumentProcess] = Result(
            status_code=status.HTTP_201_CREATED,
            message="DocumentProcessManagement.create_one_raw: Succeed.",
            data=created_document_process,
        )
        return result

    async def patch_one_by_id(self, session: AsyncSession, id: UUID, body: PatchOneBody) -> Result[DocumentProcess]:
        try:
            document_process_to_patch: DocumentProcess = DocumentProcess(**body.dict())
            patched_document_process: DocumentProcess = await self.document_process_repository.patch_one_by_id(
                session=session,
                id=id,
                document_process_to_patch=document_process_to_patch
            )
            result: Result[DocumentProcess] = Result(
                status_code=status.HTTP_200_OK,
                message="DocumentProcessManagement.patch_one_by_id: Succeed.",
                data=patched_document_process,
            )
        except exc.NoResultFound:
            result: Result[DocumentProcess] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="DocumentProcessManagement.patch_one_by_id: Failed, document_process is not found.",
                data=None,
            )
        return result

    async def patch_one_by_id_raw(self, session: AsyncSession, id: UUID, document_process_to_patch: DocumentProcess) -> \
            Result[DocumentProcess]:
        try:
            patched_document_process: DocumentProcess = await self.document_process_repository.patch_one_by_id(
                session=session,
                id=id,
                document_process_to_patch=document_process_to_patch
            )
            result: Result[DocumentProcess] = Result(
                status_code=status.HTTP_200_OK,
                message="DocumentProcessManagement.patch_one_by_id_raw: Succeed.",
                data=patched_document_process,
            )
        except exc.NoResultFound:
            result: Result[DocumentProcess] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="DocumentProcessManagement.patch_one_by_id_raw: Failed, document_process is not found.",
                data=None,
            )
        return result

    async def delete_one_by_id(self, session: AsyncSession, id: UUID) -> Result[DocumentProcess]:
        try:
            deleted_document_process: DocumentProcess = await self.document_process_repository.delete_one_by_id(
                session=session,
                id=id
            )
            result: Result[DocumentProcess] = Result(
                status_code=status.HTTP_200_OK,
                message="DocumentProcessManagement.delete_one_by_id: Succeed.",
                data=deleted_document_process,
            )
        except exc.NoResultFound:
            result: Result[DocumentProcess] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="DocumentProcessManagement.delete_one_by_id: Failed, document_process is not found.",
                data=None,
            )
        return result
