import uuid
from uuid import UUID

from sqlalchemy import exc
from starlette import status
from starlette.datastructures import State

from apps.inners.models.daos.document_process import DocumentProcess
from apps.inners.models.dtos.contracts.requests.managements.document_processes.create_one_body import CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.document_processes.patch_one_body import PatchOneBody
from apps.inners.models.dtos.contracts.result import Result
from apps.outers.repositories.document_process_repository import DocumentProcessRepository


class DocumentProcessManagement:
    def __init__(
            self,
            document_process_repository: DocumentProcessRepository,
    ):
        self.document_process_repository: DocumentProcessRepository = document_process_repository

    async def find_one_by_id(self, state: State, id: UUID) -> Result[DocumentProcess]:
        try:
            found_document_process: DocumentProcess = await self.document_process_repository.find_one_by_id(
                session=state.session,
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

    async def create_one(self, state: State, body: CreateOneBody) -> Result[DocumentProcess]:
        document_process_creator: DocumentProcess = DocumentProcess(**body.dict())
        document_process_creator.id = uuid.uuid4()
        created_document_process: DocumentProcess = await self.document_process_repository.create_one(
            session=state.session,
            document_process_creator=document_process_creator
        )
        result: Result[DocumentProcess] = Result(
            status_code=status.HTTP_201_CREATED,
            message="DocumentProcessManagement.create_one: Succeed.",
            data=created_document_process,
        )
        return result

    async def create_one_raw(self, state: State, document_process_creator: DocumentProcess) -> Result[
        DocumentProcess]:
        created_document_process: DocumentProcess = await self.document_process_repository.create_one(
            session=state.session,
            document_process_creator=document_process_creator
        )
        result: Result[DocumentProcess] = Result(
            status_code=status.HTTP_201_CREATED,
            message="DocumentProcessManagement.create_one_raw: Succeed.",
            data=created_document_process,
        )
        return result

    async def patch_one_by_id(self, state: State, id: UUID, body: PatchOneBody) -> Result[DocumentProcess]:
        try:
            document_process_patcher: DocumentProcess = DocumentProcess(**body.dict())
            patched_document_process: DocumentProcess = await self.document_process_repository.patch_one_by_id(
                session=state.session,
                id=id,
                document_process_patcher=document_process_patcher
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

    async def patch_one_by_id_raw(self, state: State, id: UUID, document_process_patcher: DocumentProcess) -> \
            Result[DocumentProcess]:
        try:
            patched_document_process: DocumentProcess = await self.document_process_repository.patch_one_by_id(
                session=state.session,
                id=id,
                document_process_patcher=document_process_patcher
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

    async def delete_one_by_id(self, state: State, id: UUID) -> Result[DocumentProcess]:
        try:
            deleted_document_process: DocumentProcess = await self.document_process_repository.delete_one_by_id(
                session=state.session,
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
