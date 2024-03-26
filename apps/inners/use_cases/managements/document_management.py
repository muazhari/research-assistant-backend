import uuid
from uuid import UUID

from sqlalchemy import exc
from starlette import status
from starlette.datastructures import State

from apps.inners.models.daos.document import Document
from apps.inners.models.dtos.contracts.requests.managements.documents.create_one_body import CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.documents.patch_one_body import PatchOneBody
from apps.inners.models.dtos.contracts.result import Result
from apps.outers.repositories.document_repository import DocumentRepository


class DocumentManagement:
    def __init__(
            self,
            document_repository: DocumentRepository,
    ):
        self.document_repository: DocumentRepository = document_repository

    async def find_one_by_id(self, state: State, id: UUID) -> Result[Document]:
        try:
            found_document: Document = await self.document_repository.find_one_by_id(
                session=state.session,
                id=id
            )
            result: Result[Document] = Result(
                status_code=status.HTTP_200_OK,
                message="DocumentManagement.find_one_by_id: Succeed.",
                data=found_document,
            )
        except exc.NoResultFound:
            result: Result[Document] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="DocumentManagement.find_one_by_id: Failed, document is not found.",
                data=None,
            )
        return result

    async def create_one(self, state: State, body: CreateOneBody) -> Result[Document]:
        document_creator: Document = Document(**body.dict())
        document_creator.id = uuid.uuid4()
        created_document: Document = await self.document_repository.create_one(
            session=state.session,
            document_creator=document_creator
        )
        result: Result[Document] = Result(
            status_code=status.HTTP_201_CREATED,
            message="DocumentManagement.create_one: Succeed.",
            data=created_document,
        )
        return result

    async def create_one_raw(self, state: State, document_creator: Document) -> Result[Document]:
        created_document: Document = await self.document_repository.create_one(
            session=state.session,
            document_creator=document_creator
        )
        result: Result[Document] = Result(
            status_code=status.HTTP_201_CREATED,
            message="DocumentManagement.create_one_raw: Succeed.",
            data=created_document,
        )
        return result

    async def patch_one_by_id(self, state: State, id: UUID, body: PatchOneBody) -> Result[Document]:
        try:
            document_patcher: Document = Document(**body.dict())
            patched_document: Document = await self.document_repository.patch_one_by_id(
                session=state.session,
                id=id,
                document_patcher=document_patcher
            )
            result: Result[Document] = Result(
                status_code=status.HTTP_200_OK,
                message="DocumentManagement.patch_one_by_id: Succeed.",
                data=patched_document,
            )
        except exc.NoResultFound:
            result: Result[Document] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="DocumentManagement.patch_one_by_id: Failed, document is not found.",
                data=None,
            )
        return result

    async def patch_one_by_id_raw(self, state: State, id: UUID, document_patcher: Document) -> Result[
        Document]:
        patched_document: Document = await self.document_repository.patch_one_by_id(
            session=state.session,
            id=id,
            document_patcher=document_patcher
        )
        result: Result[Document] = Result(
            status_code=status.HTTP_200_OK,
            message="DocumentManagement.patch_one_by_id_raw: Succeed.",
            data=patched_document,
        )
        return result

    async def delete_one_by_id(self, state: State, id: UUID) -> Result[Document]:
        try:
            deleted_document: Document = await self.document_repository.delete_one_by_id(
                session=state.session,
                id=id
            )
            result: Result[Document] = Result(
                status_code=status.HTTP_200_OK,
                message="DocumentManagement.delete_one_by_id: Succeed.",
                data=deleted_document,
            )
        except exc.NoResultFound:
            result: Result[Document] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="DocumentManagement.delete_one_by_id: Failed, document is not found.",
                data=None,
            )
        return result
