import hashlib
import uuid
from uuid import UUID

from starlette.datastructures import State

from apps.inners.models.daos.document import Document
from apps.inners.models.daos.web_document import WebDocument
from apps.inners.models.dtos.constants.document_type_constant import DocumentTypeConstant
from apps.inners.models.dtos.contracts.requests.managements.web_documents.create_one_body import CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.web_documents.patch_one_body import PatchOneBody
from apps.inners.models.dtos.contracts.responses.managements.documents.web_document_response import WebDocumentResponse
from apps.inners.use_cases.managements.document_management import DocumentManagement
from apps.outers.repositories.web_document_repository import WebDocumentRepository


class WebDocumentManagement:
    def __init__(
            self,
            document_management: DocumentManagement,
            web_document_repository: WebDocumentRepository,
    ):
        self.document_management: DocumentManagement = document_management
        self.web_document_repository: WebDocumentRepository = web_document_repository

    async def find_one_by_id_with_authorization(self, state: State, id: UUID) -> WebDocumentResponse:
        found_document: Document = await self.document_management.find_one_by_id_with_authorization(
            state=state,
            id=id
        )
        found_web_document: WebDocument = await self.web_document_repository.find_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id
        )
        found_web_document_response: WebDocumentResponse = WebDocumentResponse(
            id=found_document.id,
            document_name=found_document.name,
            document_description=found_document.description,
            document_type_id=found_document.document_type_id,
            document_account_id=found_document.account_id,
            web_url=found_web_document.web_url,
            web_url_hash=found_web_document.web_url_hash
        )
        return found_web_document_response

    async def create_one(self, state: State, body: CreateOneBody) -> WebDocumentResponse:
        document_creator: Document = Document(
            id=uuid.uuid4(),
            name=body.name,
            description=body.description,
            document_type_id=DocumentTypeConstant.WEB,
            account_id=body.account_id
        )
        created_document: Document = self.document_management.create_one_raw(
            state=state,
            document_creator=document_creator
        )
        web_document_creator: WebDocument = WebDocument(
            id=created_document.id,
            web_url=body.web_url,
            web_url_hash=hashlib.sha256(body.web_url.encode()).hexdigest()
        )
        created_web_document: WebDocument = self.create_one_raw(
            state=state,
            web_document_creator=web_document_creator
        )
        web_document_response: WebDocumentResponse = WebDocumentResponse(
            id=created_document.id,
            document_name=created_document.name,
            document_description=created_document.description,
            document_type_id=created_document.document_type_id,
            document_account_id=created_document.account_id,
            web_url=created_web_document.web_url,
            web_url_hash=created_web_document.web_url_hash
        )
        return web_document_response

    def create_one_raw(self, state: State, web_document_creator: WebDocument) -> WebDocument:
        created_web_document: WebDocument = self.web_document_repository.create_one(
            session=state.session,
            web_document_creator=web_document_creator
        )
        return created_web_document

    async def patch_one_by_id_with_authorization(self, state: State, id: UUID,
                                                 body: PatchOneBody) -> WebDocumentResponse:
        document_patcher: Document = Document(
            id=id,
            name=body.name,
            description=body.description,
            document_type_id=DocumentTypeConstant.WEB,
            account_id=body.account_id
        )
        patched_document: Document = await self.document_management.patch_one_by_id_raw_with_authorization(
            state=state,
            id=id,
            document_patcher=document_patcher
        )
        web_document_patcher: WebDocument = WebDocument(
            id=id,
            web_url=body.web_url,
            web_url_hash=hashlib.sha256(body.web_url.encode()).hexdigest()
        )
        patched_web_document: WebDocument = await self.patch_one_by_id_raw_with_authorization(
            state=state,
            id=id,
            web_document_patcher=web_document_patcher
        )
        patched_web_document_response: WebDocumentResponse = WebDocumentResponse(
            id=patched_document.id,
            document_name=patched_document.name,
            document_description=patched_document.description,
            document_type_id=patched_document.document_type_id,
            document_account_id=patched_document.account_id,
            web_url=patched_web_document.web_url,
            web_url_hash=patched_web_document.web_url_hash
        )
        return patched_web_document_response

    async def patch_one_by_id_raw_with_authorization(self, state: State, id: UUID,
                                                     web_document_patcher: WebDocument) -> WebDocument:
        patched_web_document: WebDocument = await self.web_document_repository.patch_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id,
            web_document_patcher=web_document_patcher,
        )
        return patched_web_document

    async def delete_one_by_id_with_authorization(self, state: State, id: UUID) -> WebDocumentResponse:
        deleted_web_document: WebDocument = await self.web_document_repository.delete_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id
        )
        deleted_document: Document = await self.document_management.delete_one_by_id_with_authorization(
            state=state,
            id=id
        )
        deleted_web_document_response: WebDocumentResponse = WebDocumentResponse(
            id=deleted_web_document.id,
            document_name=deleted_document.name,
            document_description=deleted_document.description,
            document_type_id=deleted_document.document_type_id,
            document_account_id=deleted_document.account_id,
            web_url=deleted_web_document.web_url,
            web_url_hash=deleted_web_document.web_url_hash
        )
        return deleted_web_document_response
