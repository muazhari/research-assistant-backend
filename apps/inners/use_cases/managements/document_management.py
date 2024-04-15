import uuid
from typing import List
from uuid import UUID

from starlette.datastructures import State

from apps.inners.models.daos.document import Document
from apps.inners.models.dtos.contracts.requests.managements.documents.create_one_body import CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.documents.patch_one_body import PatchOneBody
from apps.outers.repositories.document_repository import DocumentRepository


class DocumentManagement:
    def __init__(
            self,
            document_repository: DocumentRepository,
    ):
        self.document_repository: DocumentRepository = document_repository

    async def find_many_with_authorization_and_pagination(self, state: State, page_number: int, page_size: int) -> List[
        Document]:
        found_documents: List[Document] = await self.document_repository.find_many_by_account_id_with_pagination(
            session=state.session,
            account_id=state.authorized_session.account_id,
            page_number=page_number,
            page_size=page_size
        )

        return found_documents

    async def find_one_by_id_with_authorization(self, state: State, id: UUID) -> Document:
        found_document: Document = await self.document_repository.find_one_by_id_and_accound_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id
        )

        return found_document

    async def create_one(self, state: State, body: CreateOneBody) -> Document:
        document_creator: Document = Document(**body.dict())
        document_creator.id = uuid.uuid4()
        created_document: Document = self.create_one_raw(
            state=state,
            document_creator=document_creator
        )

        return created_document

    def create_one_raw(self, state: State, document_creator: Document) -> Document:
        created_document: Document = self.document_repository.create_one(
            session=state.session,
            document_creator=document_creator
        )

        return created_document

    async def patch_one_by_id_with_authorization(self, state: State, id: UUID, body: PatchOneBody) -> Document:
        document_patcher: Document = Document(**body.dict())
        patched_document: Document = await self.patch_one_by_id_raw_with_authorization(
            state=state,
            id=id,
            document_patcher=document_patcher
        )

        return patched_document

    async def patch_one_by_id_raw_with_authorization(self, state: State, id: UUID,
                                                     document_patcher: Document) -> Document:
        patched_document: Document = await self.document_repository.patch_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id,
            document_patcher=document_patcher,
        )

        return patched_document

    async def delete_one_by_id_with_authorization(self, state: State, id: UUID) -> Document:
        deleted_document: Document = await self.document_repository.delete_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id
        )

        return deleted_document
