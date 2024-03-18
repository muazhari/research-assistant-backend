import hashlib
import uuid
from uuid import UUID

from sqlalchemy import exc
from starlette import status
from starlette.datastructures import State

from app.inners.models.daos.document import Document
from app.inners.models.daos.text_document import TextDocument
from app.inners.models.dtos.contracts.requests.managements.text_documents.create_one_body import CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.text_documents.patch_one_body import PatchOneBody
from app.inners.models.dtos.contracts.responses.managements.documents.text_document_response import TextDocumentResponse
from app.inners.models.dtos.contracts.result import Result
from app.inners.use_cases.managements.document_management import DocumentManagement
from app.outers.interfaces.deliveries.middlewares.session_middleware import SessionMiddleware
from app.outers.repositories.text_document_repository import TextDocumentRepository


class TextDocumentManagement:
    def __init__(
            self,
            document_management: DocumentManagement,
            text_document_repository: TextDocumentRepository,
    ):
        self.document_management: DocumentManagement = document_management
        self.text_document_repository: TextDocumentRepository = text_document_repository

    async def find_one_by_id(self, state: State, id: UUID) -> Result[TextDocumentResponse]:
        try:
            found_document: Result[Document] = await self.document_management.find_one_by_id(
                state=state,
                id=id
            )
            if found_document.status_code != status.HTTP_200_OK:
                return Result(
                    status_code=found_document.status_code,
                    message=f"TextDocumentManagement.find_one_by_id: Failed, {found_document.message}",
                    data=None,
                )
            found_text_document: TextDocument = await self.text_document_repository.find_one_by_id(
                session=state.session,
                id=id
            )
            found_text_document_response: TextDocumentResponse = TextDocumentResponse(
                id=found_document.data.id,
                document_name=found_document.data.name,
                document_description=found_document.data.description,
                document_type_id=found_document.data.document_type_id,
                document_account_id=found_document.data.account_id,
                text_content=found_text_document.text_content,
                text_content_hash=found_text_document.text_content_hash
            )
            result: Result[TextDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="TextDocumentManagement.find_one_by_id: Succeed.",
                data=found_text_document_response,
            )
        except exc.NoResultFound:
            result: Result[TextDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="TextDocumentManagement.find_one_by_id: Failed, text_document is not found.",
                data=None,
            )
        return result

    async def create_one(self, state: State, body: CreateOneBody) -> Result[TextDocumentResponse]:
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
            result: Result[TextDocumentResponse] = Result(
                status_code=created_document.status_code,
                message=f"TextDocumentManagement.create_one: Failed, {created_document.message}",
                data=None,
            )
            raise SessionMiddleware.HandlerException(
                result=result
            )

        text_document_creator: TextDocument = TextDocument(
            id=created_document.data.id,
            text_content=body.text_content,
            text_content_hash=hashlib.sha256(body.text_content.encode()).hexdigest()
        )
        created_text_document: TextDocument = await self.text_document_repository.create_one(
            session=state.session,
            text_document_creator=text_document_creator
        )
        text_document_response: TextDocumentResponse = TextDocumentResponse(
            id=created_document.data.id,
            document_name=created_document.data.name,
            document_description=created_document.data.description,
            document_type_id=created_document.data.document_type_id,
            document_account_id=created_document.data.account_id,
            text_content=created_text_document.text_content,
            text_content_hash=created_text_document.text_content_hash
        )
        result: Result[TextDocumentResponse] = Result(
            status_code=status.HTTP_201_CREATED,
            message="TextDocumentManagement.create_one: Succeed.",
            data=text_document_response,
        )
        return result

    async def create_one_raw(self, state: State, text_document_creator: TextDocument) -> Result[
        TextDocumentResponse]:
        created_text_document: TextDocument = await self.text_document_repository.create_one(
            session=state.session,
            text_document_creator=text_document_creator
        )
        result: Result[TextDocumentResponse] = Result(
            status_code=status.HTTP_201_CREATED,
            message="TextDocumentManagement.create_one_raw: Succeed.",
            data=created_text_document,
        )
        return result

    async def patch_one_by_id(self, state: State, id: UUID, body: PatchOneBody) -> Result[
        TextDocumentResponse]:
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
                result: Result[TextDocumentResponse] = Result(
                    status_code=patched_document.status_code,
                    message=f"TextDocumentManagement.patch_one_by_id: Failed, {patched_document.message}",
                    data=None,
                )
                raise SessionMiddleware.HandlerException(
                    result=result
                )

            text_document_patcher: TextDocument = TextDocument(
                id=id,
                text_content=body.text_content,
                text_content_hash=hashlib.sha256(body.text_content.encode()).hexdigest()
            )
            patched_text_document: TextDocument = await self.text_document_repository.patch_one_by_id(
                session=state.session,
                id=id,
                text_document_patcher=text_document_patcher
            )
            patched_text_document_response: TextDocumentResponse = TextDocumentResponse(
                id=patched_document.data.id,
                document_name=patched_document.data.name,
                document_description=patched_document.data.description,
                document_type_id=patched_document.data.document_type_id,
                document_account_id=patched_document.data.account_id,
                text_content=patched_text_document.text_content,
                text_content_hash=patched_text_document.text_content_hash
            )
            result: Result[TextDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="TextDocumentManagement.patch_one_by_id: Succeed.",
                data=patched_text_document_response,
            )
        except exc.NoResultFound:
            result: Result[TextDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="TextDocumentManagement.patch_one_by_id: Failed, text_document is not found.",
                data=None,
            )
        return result

    async def patch_one_by_id_raw(self, state: State, id: UUID, text_document_patcher: TextDocument) -> \
            Result[
                TextDocumentResponse]:
        patched_text_document: TextDocument = await self.text_document_repository.patch_one_by_id(
            session=state.session,
            id=id,
            text_document_patcher=text_document_patcher
        )
        result: Result[TextDocumentResponse] = Result(
            status_code=status.HTTP_200_OK,
            message="TextDocumentManagement.patch_one_by_id_raw: Succeed.",
            data=patched_text_document,
        )
        return result

    async def delete_one_by_id(self, state: State, id: UUID) -> Result[TextDocumentResponse]:
        try:
            deleted_text_document: TextDocument = await self.text_document_repository.delete_one_by_id(
                session=state.session,
                id=id
            )
            deleted_document: Result[Document] = await self.document_management.delete_one_by_id(
                state=state,
                id=id
            )
            if deleted_document.status_code != status.HTTP_200_OK:
                result: Result[TextDocumentResponse] = Result(
                    status_code=deleted_document.status_code,
                    message=f"TextDocumentManagement.delete_one_by_id: Failed, {deleted_document.message}",
                    data=None,
                )
                raise SessionMiddleware.HandlerException(
                    result=result
                )

            deleted_text_document_response: TextDocumentResponse = TextDocumentResponse(
                id=deleted_text_document.id,
                document_name=deleted_document.data.name,
                document_description=deleted_document.data.description,
                document_type_id=deleted_document.data.document_type_id,
                document_account_id=deleted_document.data.account_id,
                text_content=deleted_text_document.text_content,
                text_content_hash=deleted_text_document.text_content_hash
            )
            result: Result[TextDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="TextDocumentManagement.delete_one_by_id: Succeed.",
                data=deleted_text_document_response,
            )
        except exc.NoResultFound:
            result: Result[TextDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="TextDocumentManagement.delete_one_by_id: Failed, text_document is not found.",
                data=None,
            )
        return result
