import hashlib
import uuid
from uuid import UUID

from starlette.datastructures import State

from apps.inners.models.daos.document import Document
from apps.inners.models.daos.file_document import FileDocument
from apps.inners.models.dtos.contracts.requests.managements.file_documents.create_one_body import CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.file_documents.patch_one_body import PatchOneBody
from apps.inners.models.dtos.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from apps.inners.use_cases.managements.document_management import DocumentManagement
from apps.outers.repositories.file_document_repository import FileDocumentRepository


class FileDocumentManagement:
    def __init__(
            self,
            document_management: DocumentManagement,
            file_document_repository: FileDocumentRepository,
    ):
        self.document_management: DocumentManagement = document_management
        self.file_document_repository: FileDocumentRepository = file_document_repository

    async def find_one_by_id(self, state: State, id: UUID) -> FileDocumentResponse:
        found_document: Document = await self.document_management.find_one_by_id(
            state=state,
            id=id
        )
        found_file_document: FileDocument = await self.file_document_repository.find_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id
        )
        found_file_document_response: FileDocumentResponse = FileDocumentResponse(
            id=found_document.id,
            document_name=found_document.name,
            document_description=found_document.description,
            document_type_id=found_document.document_type_id,
            document_account_id=found_document.account_id,
            file_name=found_file_document.file_name,
            file_data_hash=found_file_document.file_data_hash,
            file_meta=dict()
        )
        return found_file_document_response

    async def create_one(self, state: State, body: CreateOneBody) -> FileDocumentResponse:
        document_creator: Document = Document(
            id=uuid.uuid4(),
            name=body.document_name,
            description=body.document_description,
            document_type_id=body.document_type_id,
            account_id=body.document_account_id
        )
        created_document: Document = self.document_management.create_one_raw(
            state=state,
            document_creator=document_creator
        )
        file_data: bytes = await body.file_data.read()
        await body.file_data.close()
        file_document_creator: FileDocument = FileDocument(
            id=created_document.id,
            file_name=body.file_name,
            file_data_hash=hashlib.sha256(file_data).hexdigest()
        )
        created_file_document: FileDocument = self.create_one_raw(
            state=state,
            file_document_creator=file_document_creator,
            file_data=file_data
        )
        file_document_response: FileDocumentResponse = FileDocumentResponse(
            id=created_document.id,
            document_name=created_document.name,
            document_description=created_document.description,
            document_type_id=created_document.document_type_id,
            document_account_id=created_document.account_id,
            file_name=created_file_document.file_name,
            file_data_hash=created_file_document.file_data_hash,
            file_meta=dict()
        )
        return file_document_response

    def create_one_raw(self, state: State, file_document_creator: FileDocument,
                       file_data: bytes) -> FileDocument:
        created_file_document: FileDocument = self.file_document_repository.create_one(
            session=state.session,
            file_document_creator=file_document_creator,
            file_data=file_data
        )
        return created_file_document

    async def patch_one_by_id(self, state: State, id: UUID, body: PatchOneBody) -> FileDocumentResponse:
        document_patcher: Document = Document(
            id=id,
            name=body.document_name,
            description=body.document_description,
            document_type_id=body.document_type_id,
            account_id=body.document_account_id
        )
        patched_document: Document = await self.document_management.patch_one_by_id_raw(
            state=state,
            id=id,
            document_patcher=document_patcher
        )
        file_data: bytes = await body.file_data.read()
        await body.file_data.close()
        file_document_patcher: FileDocument = FileDocument(
            file_name=body.file_name,
            file_data_hash=hashlib.sha256(file_data).hexdigest()
        )
        patched_file_document: FileDocument = await self.patch_one_by_id_raw(
            state=state,
            id=id,
            file_document_patcher=file_document_patcher,
            file_data=file_data
        )
        patched_file_document_response: FileDocumentResponse = FileDocumentResponse(
            id=patched_document.id,
            document_name=patched_document.name,
            document_description=patched_document.description,
            document_type_id=patched_document.document_type_id,
            document_account_id=patched_document.account_id,
            file_name=patched_file_document.file_name,
            file_data_hash=patched_file_document.file_data_hash,
            file_meta=dict()
        )
        return patched_file_document_response

    async def patch_one_by_id_raw(self, state: State, id: UUID, file_document_patcher: FileDocument,
                                  file_data: bytes) -> FileDocument:
        patched_file_document: FileDocument = await self.file_document_repository.patch_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id,
            file_document_patcher=file_document_patcher,
            file_data=file_data
        )
        return patched_file_document

    async def delete_one_by_id(self, state: State, id: UUID) -> FileDocumentResponse:
        deleted_file_document: FileDocument = await self.file_document_repository.delete_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id
        )
        deleted_document: Document = await self.document_management.delete_one_by_id(
            state=state,
            id=id
        )
        deleted_file_document_response: FileDocumentResponse = FileDocumentResponse(
            id=deleted_document.id,
            document_name=deleted_document.name,
            document_description=deleted_document.description,
            document_type_id=deleted_document.document_type_id,
            document_account_id=deleted_document.account_id,
            file_name=deleted_file_document.file_name,
            file_data_hash=deleted_file_document.file_data_hash,
            file_meta=dict()
        )
        return deleted_file_document_response
