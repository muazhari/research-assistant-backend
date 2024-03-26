import hashlib
import uuid
from uuid import UUID

from sqlalchemy import exc
from starlette import status
from starlette.datastructures import State

from apps.inners.models.daos.document import Document
from apps.inners.models.daos.web_document import WebDocument
from apps.inners.models.dtos.contracts.requests.managements.web_documents.create_one_body import CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.web_documents.patch_one_body import PatchOneBody
from apps.inners.models.dtos.contracts.responses.managements.documents.web_document_response import WebDocumentResponse
from apps.inners.models.dtos.contracts.result import Result
from apps.inners.use_cases.managements.document_management import DocumentManagement
from apps.outers.interfaces.deliveries.middlewares.session_middleware import SessionMiddleware
from apps.outers.repositories.web_document_repository import WebDocumentRepository


class WebDocumentManagement:
    def __init__(
            self,
            document_management: DocumentManagement,
            web_document_repository: WebDocumentRepository,
    ):
        self.document_management: DocumentManagement = document_management
        self.web_document_repository: WebDocumentRepository = web_document_repository

    async def find_one_by_id(self, state: State, id: UUID) -> Result[WebDocumentResponse]:
        try:
            found_document: Result[Document] = await self.document_management.find_one_by_id(
                state=state,
                id=id
            )
            if found_document.status_code != status.HTTP_200_OK:
                return Result(
                    status_code=found_document.status_code,
                    message=f"WebDocumentManagement.find_one_by_id: Failed, {found_document.message}",
                    data=None,
                )
            found_web_document: WebDocument = await self.web_document_repository.find_one_by_id(
                session=state.session,
                id=id
            )
            found_web_document_response: WebDocumentResponse = WebDocumentResponse(
                id=found_document.data.id,
                document_name=found_document.data.name,
                document_description=found_document.data.description,
                document_type_id=found_document.data.document_type_id,
                document_account_id=found_document.data.account_id,
                web_url=found_web_document.web_url,
                web_url_hash=found_web_document.web_url_hash
            )
            result: Result[WebDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="WebDocumentManagement.find_one_by_id: Succeed.",
                data=found_web_document_response,
            )
        except exc.NoResultFound:
            result: Result[WebDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="WebDocumentManagement.find_one_by_id: Failed, web_document is not found.",
                data=None,
            )
        return result

    async def create_one(self, state: State, body: CreateOneBody) -> Result[WebDocumentResponse]:
        document_creator: Document = Document(
            id=uuid.uuid4(),
            name=body.name,
            description=body.description,
            document_type_id=body.document_type_id,
            account_id=body.account_id
        )
        created_document: Result[Document] = await self.document_management.create_one_raw(
            state=state,
            document_creator=document_creator
        )
        if created_document.status_code != status.HTTP_201_CREATED:
            result: Result[WebDocumentResponse] = Result(
                status_code=created_document.status_code,
                message=f"WebDocumentManagement.create_one: Failed, {created_document.message}",
                data=None,
            )
            raise SessionMiddleware.HandlerException(
                result=result
            )

        web_document_creator: WebDocument = WebDocument(
            id=created_document.data.id,
            web_url=body.web_url,
            web_url_hash=hashlib.sha256(body.web_url.encode()).hexdigest()
        )
        created_web_document: WebDocument = await self.web_document_repository.create_one(
            session=state.session,
            web_document_creator=web_document_creator
        )
        web_document_response: WebDocumentResponse = WebDocumentResponse(
            id=created_document.data.id,
            document_name=created_document.data.name,
            document_description=created_document.data.description,
            document_type_id=created_document.data.document_type_id,
            document_account_id=created_document.data.account_id,
            web_url=created_web_document.web_url,
            web_url_hash=created_web_document.web_url_hash
        )
        result: Result[WebDocumentResponse] = Result(
            status_code=status.HTTP_201_CREATED,
            message="WebDocumentManagement.create_one: Succeed.",
            data=web_document_response,
        )
        return result

    async def create_one_raw(self, state: State, web_document_creator: WebDocument) -> Result[
        WebDocumentResponse]:
        created_web_document: WebDocument = await self.web_document_repository.create_one(
            session=state.session,
            web_document_creator=web_document_creator
        )
        result: Result[WebDocumentResponse] = Result(
            status_code=status.HTTP_201_CREATED,
            message="WebDocumentManagement.create_one_raw: Succeed.",
            data=created_web_document,
        )
        return result

    async def patch_one_by_id(self, state: State, id: UUID, body: PatchOneBody) -> Result[
        WebDocumentResponse]:
        try:
            document_patcher: Document = Document(
                id=id,
                name=body.name,
                description=body.description,
                document_type_id=body.document_type_id,
                account_id=body.account_id
            )
            patched_document: Result[Document] = await self.document_management.patch_one_by_id_raw(
                state=state,
                id=id,
                document_patcher=document_patcher
            )
            if patched_document.status_code != status.HTTP_200_OK:
                result: Result[WebDocumentResponse] = Result(
                    status_code=patched_document.status_code,
                    message=f"WebDocumentManagement.patch_one_by_id: Failed, {patched_document.message}",
                    data=None,
                )
                raise SessionMiddleware.HandlerException(
                    result=result
                )

            web_document_patcher: WebDocument = WebDocument(
                id=id,
                web_url=body.web_url,
                web_url_hash=hashlib.sha256(body.web_url.encode()).hexdigest()
            )
            patched_web_document: WebDocument = await self.web_document_repository.patch_one_by_id(
                session=state.session,
                id=id,
                web_document_patcher=web_document_patcher
            )
            patched_web_document_response: WebDocumentResponse = WebDocumentResponse(
                id=patched_document.data.id,
                document_name=patched_document.data.name,
                document_description=patched_document.data.description,
                document_type_id=patched_document.data.document_type_id,
                document_account_id=patched_document.data.account_id,
                web_url=patched_web_document.web_url,
                web_url_hash=patched_web_document.web_url_hash
            )
            result: Result[WebDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="WebDocumentManagement.patch_one_by_id: Succeed.",
                data=patched_web_document_response,
            )
        except exc.NoResultFound:
            result: Result[WebDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="WebDocumentManagement.patch_one_by_id: Failed, web_document is not found.",
                data=None,
            )
        return result

    async def patch_one_by_id_raw(self, state: State, id: UUID, web_document_patcher: WebDocument) -> \
            Result[
                WebDocumentResponse]:
        patched_web_document: WebDocument = await self.web_document_repository.patch_one_by_id(
            session=state.session,
            id=id,
            web_document_patcher=web_document_patcher
        )
        result: Result[WebDocumentResponse] = Result(
            status_code=status.HTTP_200_OK,
            message="WebDocumentManagement.patch_one_by_id_raw: Succeed.",
            data=patched_web_document,
        )
        return result

    async def delete_one_by_id(self, state: State, id: UUID) -> Result[WebDocumentResponse]:
        try:
            deleted_web_document: WebDocument = await self.web_document_repository.delete_one_by_id(
                session=state.session,
                id=id
            )
            deleted_document: Result[Document] = await self.document_management.delete_one_by_id(
                state=state,
                id=id
            )
            if deleted_document.status_code != status.HTTP_200_OK:
                result: Result[WebDocumentResponse] = Result(
                    status_code=deleted_document.status_code,
                    message=f"WebDocumentManagement.delete_one_by_id: Failed, {deleted_document.message}",
                    data=None,
                )
                raise SessionMiddleware.HandlerException(
                    result=result
                )

            deleted_web_document_response: WebDocumentResponse = WebDocumentResponse(
                id=deleted_web_document.id,
                document_name=deleted_document.data.name,
                document_description=deleted_document.data.description,
                document_type_id=deleted_document.data.document_type_id,
                document_account_id=deleted_document.data.account_id,
                web_url=deleted_web_document.web_url,
                web_url_hash=deleted_web_document.web_url_hash
            )
            result: Result[WebDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="WebDocumentManagement.delete_one_by_id: Succeed.",
                data=deleted_web_document_response,
            )
        except exc.NoResultFound:
            result: Result[WebDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="WebDocumentManagement.delete_one_by_id: Failed, web_document is not found.",
                data=None,
            )
        return result
