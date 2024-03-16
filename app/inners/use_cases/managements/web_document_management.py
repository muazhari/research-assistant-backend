from uuid import UUID

from sqlalchemy import exc
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from app.inners.models.daos.web_document import WebDocument
from app.inners.models.dtos.contracts.requests.managements.web_documents.create_one_body import CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.web_documents.patch_one_body import PatchOneBody
from app.inners.models.dtos.contracts.responses.managements.documents.web_document_response import WebDocumentResponse
from app.inners.models.dtos.contracts.result import Result
from app.inners.use_cases.managements.document_management import DocumentManagement
from app.outers.repositories.web_document_repository import WebDocumentRepository


class WebDocumentManagement:
    def __init__(
            self,
            document_management: DocumentManagement,
            web_document_repository: WebDocumentRepository,
    ):
        self.document_management: DocumentManagement = document_management
        self.web_document_repository: WebDocumentRepository = web_document_repository

    async def find_one_by_id(self, session: AsyncSession, id: UUID) -> Result[WebDocumentResponse]:
        try:
            found_web_document: WebDocument = await self.web_document_repository.find_one_by_id(
                session=session,
                id=id
            )
            result: Result[WebDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="WebDocumentManagement.find_one_by_id: Succeed.",
                data=found_web_document,
            )
        except exc.NoResultFound:
            result: Result[WebDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="WebDocumentManagement.find_one_by_id: Failed, web_document is not found.",
                data=None,
            )
        return result

    async def create_one(self, session: AsyncSession, body: CreateOneBody) -> Result[WebDocumentResponse]:
        web_document_to_create: WebDocument = WebDocument(**body.dict())
        created_web_document: WebDocument = await self.web_document_repository.create_one(
            session=session,
            web_document_to_create=web_document_to_create
        )
        result: Result[WebDocumentResponse] = Result(
            status_code=status.HTTP_201_CREATED,
            message="WebDocumentManagement.create_one: Succeed.",
            data=created_web_document,
        )
        return result

    async def create_one_raw(self, session: AsyncSession, web_document_to_create: WebDocument) -> Result[
        WebDocumentResponse]:
        created_web_document: WebDocument = await self.web_document_repository.create_one(
            session=session,
            web_document_to_create=web_document_to_create
        )
        result: Result[WebDocumentResponse] = Result(
            status_code=status.HTTP_201_CREATED,
            message="WebDocumentManagement.create_one_raw: Succeed.",
            data=created_web_document,
        )
        return result

    async def patch_one_by_id(self, session: AsyncSession, id: UUID, body: PatchOneBody) -> Result[WebDocumentResponse]:
        try:
            web_document_to_patch: WebDocument = WebDocument(**body.dict())
            patched_web_document: WebDocument = await self.web_document_repository.patch_one_by_id(
                session=session,
                id=id,
                web_document_to_patch=web_document_to_patch
            )
            result: Result[WebDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="WebDocumentManagement.patch_one_by_id: Succeed.",
                data=patched_web_document,
            )
        except exc.NoResultFound:
            result: Result[WebDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="WebDocumentManagement.patch_one_by_id: Failed, web_document is not found.",
                data=None,
            )
        return result

    async def patch_one_by_id_raw(self, session: AsyncSession, id: UUID, web_document_to_patch: WebDocument) -> Result[
        WebDocumentResponse]:
        try:
            patched_web_document: WebDocument = await self.web_document_repository.patch_one_by_id(
                session=session,
                id=id,
                web_document_to_patch=web_document_to_patch
            )
            result: Result[WebDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="WebDocumentManagement.patch_one_by_id: Succeed.",
                data=patched_web_document,
            )
        except exc.NoResultFound:
            result: Result[WebDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="WebDocumentManagement.patch_one_by_id: Failed, web_document is not found.",
                data=None,
            )
        return result

    async def delete_one_by_id(self, session: AsyncSession, id: UUID) -> Result[WebDocumentResponse]:
        try:
            deleted_web_document: WebDocument = await self.web_document_repository.delete_one_by_id(
                session=session,
                id=id
            )
            result: Result[WebDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="WebDocumentManagement.delete_one_by_id: Succeed.",
                data=deleted_web_document,
            )
        except exc.NoResultFound:
            result: Result[WebDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="WebDocumentManagement.delete_one_by_id: Failed, web_document is not found.",
                data=None,
            )
        return result
