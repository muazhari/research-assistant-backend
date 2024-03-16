from uuid import UUID

from sqlalchemy import exc
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from app.inners.models.daos.text_document import TextDocument
from app.inners.models.dtos.contracts.requests.managements.text_documents.create_one_body import CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.text_documents.patch_one_body import PatchOneBody
from app.inners.models.dtos.contracts.responses.managements.documents.text_document_response import TextDocumentResponse
from app.inners.models.dtos.contracts.result import Result
from app.inners.use_cases.managements.document_management import DocumentManagement
from app.outers.repositories.text_document_repository import TextDocumentRepository


class TextDocumentManagement:
    def __init__(
            self,
            document_management: DocumentManagement,
            text_document_repository: TextDocumentRepository,
    ):
        self.document_management: DocumentManagement = document_management
        self.text_document_repository: TextDocumentRepository = text_document_repository

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> Result[TextDocumentResponse]:
        try:
            found_text_document: TextDocument = await self.text_document_repository.find_one_by_id(
                session=session,
                id=id
            )
            result: Result[TextDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="TextDocumentManagement.find_one_by_id: Succeed.",
                data=found_text_document,
            )
        except exc.NoResultFound:
            result: Result[TextDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="TextDocumentManagement.find_one_by_id: Failed, text_document is not found.",
                data=None,
            )
        return result

    async def create_one(self, session: AsyncSession, body: CreateOneBody) -> Result[TextDocumentResponse]:
        text_document_to_create: TextDocument = TextDocument(**body.dict())
        created_text_document: TextDocument = await self.text_document_repository.create_one(
            session=session,
            text_document_to_create=text_document_to_create
        )
        result: Result[TextDocumentResponse] = Result(
            status_code=status.HTTP_201_CREATED,
            message="TextDocumentManagement.create_one: Succeed.",
            data=created_text_document,
        )
        return result

    async def create_one_raw(self, session: AsyncSession, text_document_to_create: TextDocument) -> Result[
        TextDocumentResponse]:
        created_text_document: TextDocument = await self.text_document_repository.create_one(
            session=session,
            text_document_to_create=text_document_to_create
        )
        result: Result[TextDocumentResponse] = Result(
            status_code=status.HTTP_201_CREATED,
            message="TextDocumentManagement.create_one_raw: Succeed.",
            data=created_text_document,
        )
        return result

    async def patch_one_by_id(self, session: AsyncSession, id: UUID, body: PatchOneBody) -> Result[
        TextDocumentResponse]:
        try:
            text_document_to_patch: TextDocument = TextDocument(**body.dict())
            patched_text_document: TextDocument = await self.text_document_repository.patch_one_by_id(
                session=session,
                id=id,
                text_document_to_patch=text_document_to_patch
            )
            result: Result[TextDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="TextDocumentManagement.patch_one_by_id: Succeed.",
                data=patched_text_document,
            )
        except exc.NoResultFound:
            result: Result[TextDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="TextDocumentManagement.patch_one_by_id: Failed, text_document is not found.",
                data=None,
            )
        return result

    async def patch_one_by_id_raw(self, session: AsyncSession, id: UUID, text_document_to_patch: TextDocument) -> \
            Result[
                TextDocumentResponse]:
        try:
            patched_text_document: TextDocument = await self.text_document_repository.patch_one_by_id(
                session=session,
                id=id,
                text_document_to_patch=text_document_to_patch
            )
            result: Result[TextDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="TextDocumentManagement.patch_one_by_id_raw: Succeed.",
                data=patched_text_document,
            )
        except exc.NoResultFound:
            result: Result[TextDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="TextDocumentManagement.patch_one_by_id_raw: Failed, text_document is not found.",
                data=None,
            )
        return result

    async def delete_one_by_id(self, session: AsyncSession, id: UUID) -> Result[TextDocumentResponse]:
        try:
            deleted_text_document: TextDocument = await self.text_document_repository.delete_one_by_id(
                session=session,
                id=id
            )
            result: Result[TextDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="TextDocumentManagement.delete_one_by_id: Succeed.",
                data=deleted_text_document,
            )
        except exc.NoResultFound:
            result: Result[TextDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="TextDocumentManagement.delete_one_by_id: Failed, text_document is not found.",
                data=None,
            )
        return result
