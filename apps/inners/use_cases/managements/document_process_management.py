import uuid
from uuid import UUID

from starlette.datastructures import State

from apps.inners.models.daos.document_process import DocumentProcess
from apps.inners.models.dtos.contracts.requests.managements.document_processes.create_one_body import CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.document_processes.patch_one_body import PatchOneBody
from apps.outers.repositories.document_process_repository import DocumentProcessRepository


class DocumentProcessManagement:
    def __init__(
            self,
            document_process_repository: DocumentProcessRepository,
    ):
        self.document_process_repository: DocumentProcessRepository = document_process_repository

    async def find_one_by_id_with_authorization(self, state: State, id: UUID) -> DocumentProcess:
        found_document_process: DocumentProcess = await self.document_process_repository.find_one_by_id_and_accound_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id
        )
        return found_document_process

    async def create_one(self, state: State, body: CreateOneBody) -> DocumentProcess:
        document_process_creator: DocumentProcess = DocumentProcess(**body.dict())
        document_process_creator.id = uuid.uuid4()
        created_document_process: DocumentProcess = await self.create_one_raw(
            state=state,
            document_process_creator=document_process_creator
        )
        return created_document_process

    async def create_one_raw(self, state: State, document_process_creator: DocumentProcess) -> DocumentProcess:
        created_document_process: DocumentProcess = self.document_process_repository.create_one(
            session=state.session,
            document_process_creator=document_process_creator
        )
        return created_document_process

    async def patch_one_by_id_with_authorization(self, state: State, id: UUID, body: PatchOneBody) -> DocumentProcess:
        document_process_patcher: DocumentProcess = DocumentProcess(**body.dict())
        patched_document_process: DocumentProcess = await self.patch_one_by_id_raw_with_authorization(
            state=state,
            id=id,
            document_process_patcher=document_process_patcher
        )
        return patched_document_process

    async def patch_one_by_id_raw_with_authorization(self, state: State, id: UUID,
                                                     document_process_patcher: DocumentProcess) -> DocumentProcess:
        patched_document_process: DocumentProcess = await self.document_process_repository.patch_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id,
            document_process_patcher=document_process_patcher
        )
        return patched_document_process

    async def delete_one_by_id_with_authorization(self, state: State, id: UUID) -> DocumentProcess:
        deleted_document_process: DocumentProcess = await self.document_process_repository.delete_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id
        )
        return deleted_document_process
