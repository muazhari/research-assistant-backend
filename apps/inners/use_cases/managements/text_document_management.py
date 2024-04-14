import hashlib
import uuid
from uuid import UUID

from starlette.datastructures import State

from apps.inners.models.daos.document import Document
from apps.inners.models.daos.text_document import TextDocument
from apps.inners.models.dtos.constants.document_type_constant import DocumentTypeConstant
from apps.inners.models.dtos.contracts.requests.managements.text_documents.create_one_body import CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.text_documents.patch_one_body import PatchOneBody
from apps.inners.models.dtos.contracts.responses.managements.documents.text_document_response import \
    TextDocumentResponse
from apps.inners.use_cases.managements.document_management import DocumentManagement
from apps.outers.repositories.text_document_repository import TextDocumentRepository


class TextDocumentManagement:
    def __init__(
            self,
            document_management: DocumentManagement,
            text_document_repository: TextDocumentRepository,
    ):
        self.document_management: DocumentManagement = document_management
        self.text_document_repository: TextDocumentRepository = text_document_repository

    async def find_one_by_id_with_authorization(self, state: State, id: UUID) -> TextDocumentResponse:
        found_document: Document = await self.document_management.find_one_by_id_with_authorization(
            state=state,
            id=id
        )
        found_text_document: TextDocument = await self.text_document_repository.find_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id
        )
        found_text_document_response: TextDocumentResponse = TextDocumentResponse(
            id=found_document.id,
            document_name=found_document.name,
            document_description=found_document.description,
            document_type_id=found_document.document_type_id,
            document_account_id=found_document.account_id,
            text_content=found_text_document.text_content,
            text_content_hash=found_text_document.text_content_hash
        )

        return found_text_document_response

    async def create_one(self, state: State, body: CreateOneBody) -> TextDocumentResponse:
        document_creator: Document = Document(
            id=uuid.uuid4(),
            name=body.name,
            description=body.description,
            document_type_id=DocumentTypeConstant.TEXT,
            account_id=body.account_id
        )
        created_document: Document = self.document_management.create_one_raw(
            state=state,
            document_creator=document_creator
        )
        text_document_creator: TextDocument = TextDocument(
            id=created_document.id,
            text_content=body.text_content,
            text_content_hash=hashlib.sha256(body.text_content.encode()).hexdigest()
        )
        created_text_document: TextDocument = self.create_one_raw(
            state=state,
            text_document_creator=text_document_creator
        )
        text_document_response: TextDocumentResponse = TextDocumentResponse(
            id=created_document.id,
            document_name=created_document.name,
            document_description=created_document.description,
            document_type_id=created_document.document_type_id,
            document_account_id=created_document.account_id,
            text_content=created_text_document.text_content,
            text_content_hash=created_text_document.text_content_hash
        )

        return text_document_response

    def create_one_raw(self, state: State, text_document_creator: TextDocument) -> TextDocument:
        created_text_document: TextDocument = self.text_document_repository.create_one(
            session=state.session,
            text_document_creator=text_document_creator
        )

        return created_text_document

    async def patch_one_by_id_with_authorization(self, state: State, id: UUID,
                                                 body: PatchOneBody) -> TextDocumentResponse:
        document_patcher: Document = Document(
            id=id,
            name=body.name,
            description=body.description,
            document_type_id=DocumentTypeConstant.TEXT,
            account_id=body.account_id
        )
        patched_document: Document = await self.document_management.patch_one_by_id_raw_with_authorization(
            state=state,
            id=id,
            document_patcher=document_patcher
        )
        text_document_patcher: TextDocument = TextDocument(
            id=id,
            text_content=body.text_content,
            text_content_hash=hashlib.sha256(body.text_content.encode()).hexdigest()
        )
        patched_text_document: TextDocument = await self.patch_one_by_id_raw_with_authorization(
            state=state,
            id=id,
            text_document_patcher=text_document_patcher
        )
        patched_text_document_response: TextDocumentResponse = TextDocumentResponse(
            id=patched_document.id,
            document_name=patched_document.name,
            document_description=patched_document.description,
            document_type_id=patched_document.document_type_id,
            document_account_id=patched_document.account_id,
            text_content=patched_text_document.text_content,
            text_content_hash=patched_text_document.text_content_hash
        )

        return patched_text_document_response

    async def patch_one_by_id_raw_with_authorization(self, state: State, id: UUID,
                                                     text_document_patcher: TextDocument) -> TextDocument:
        patched_text_document: TextDocument = await self.text_document_repository.patch_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id,
            text_document_patcher=text_document_patcher
        )

        return patched_text_document

    async def delete_one_by_id_with_authorization(self, state: State, id: UUID) -> TextDocumentResponse:
        deleted_text_document: TextDocument = await self.text_document_repository.delete_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id
        )
        deleted_document: Document = await self.document_management.delete_one_by_id_with_authorization(
            state=state,
            id=id
        )
        deleted_text_document_response: TextDocumentResponse = TextDocumentResponse(
            id=deleted_text_document.id,
            document_name=deleted_document.name,
            document_description=deleted_document.description,
            document_type_id=deleted_document.document_type_id,
            document_account_id=deleted_document.account_id,
            text_content=deleted_text_document.text_content,
            text_content_hash=deleted_text_document.text_content_hash
        )

        return deleted_text_document_response
