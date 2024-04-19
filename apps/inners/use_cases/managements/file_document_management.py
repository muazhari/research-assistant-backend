import hashlib
import uuid
from typing import List, Optional, Dict, Any
from uuid import UUID

from starlette.datastructures import State

from apps.inners.models.daos.document import Document
from apps.inners.models.daos.file_document import FileDocument
from apps.inners.models.dtos.constants.document_type_constant import DocumentTypeConstant
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

    def get_file_metadata(self, file_document: FileDocument) -> Dict[str, Any]:
        file_url: str = self.file_document_repository.get_object_url(
            object_name=file_document.file_name
        )
        file_metadata: Dict[str, Any] = {
            "file_url": file_url
        }
        return file_metadata

    async def find_many_with_authorization_and_pagination(self, state: State, page_position: int, page_size: int) -> \
            List[
                FileDocumentResponse]:
        found_file_documents: List[
            FileDocument
        ] = await self.file_document_repository.find_many_by_account_id_with_pagination(
            session=state.session,
            account_id=state.authorized_session.account_id,
            page_position=page_position,
            page_size=page_size
        )
        found_documents: List[
            Document
        ] = await self.document_management.document_repository.find_many_by_id_and_account_id(
            session=state.session,
            ids=[found_file_document.id for found_file_document in found_file_documents],
            account_id=state.authorized_session.account_id
        )
        found_file_document_responses: List[FileDocumentResponse] = []
        for found_document, found_file_document in zip(found_documents, found_file_documents, strict=True):
            found_file_document_response: FileDocumentResponse = FileDocumentResponse(
                id=found_document.id,
                name=found_document.name,
                description=found_document.description,
                document_type_id=found_document.document_type_id,
                account_id=found_document.account_id,
                file_name=found_file_document.file_name,
                file_data_hash=found_file_document.file_data_hash,
                file_metadata=self.get_file_metadata(found_file_document)
            )
            found_file_document_responses.append(found_file_document_response)

        return found_file_document_responses

    async def find_one_by_id_with_authorization(self, state: State, id: UUID) -> FileDocumentResponse:
        found_document: Document = await self.document_management.find_one_by_id_with_authorization(
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
            name=found_document.name,
            description=found_document.description,
            document_type_id=found_document.document_type_id,
            account_id=found_document.account_id,
            file_name=found_file_document.file_name,
            file_data_hash=found_file_document.file_data_hash,
            file_metadata=self.get_file_metadata(found_file_document)
        )
        return found_file_document_response

    async def create_one(self, state: State, body: CreateOneBody) -> FileDocumentResponse:
        document_creator: Document = Document(
            id=uuid.uuid4(),
            name=body.name,
            description=body.description,
            document_type_id=DocumentTypeConstant.FILE,
            account_id=body.account_id
        )
        created_document: Document = self.document_management.create_one_raw(
            state=state,
            document_creator=document_creator
        )
        file_data: Optional[bytes] = None
        if body.file_data is not None:
            file_data = await body.file_data.read()
            await body.file_data.close()
        file_document_creator: FileDocument = FileDocument(
            id=created_document.id,
            file_name=f"{uuid.uuid4()}_{body.file_name}",
            file_data_hash=hashlib.sha256(file_data).hexdigest()
        )
        created_file_document: FileDocument = self.create_one_raw(
            state=state,
            file_document_creator=file_document_creator,
            file_data=file_data
        )
        file_document_response: FileDocumentResponse = FileDocumentResponse(
            id=created_document.id,
            name=created_document.name,
            description=created_document.description,
            document_type_id=created_document.document_type_id,
            account_id=created_document.account_id,
            file_name=created_file_document.file_name,
            file_data_hash=created_file_document.file_data_hash,
            file_metadata=self.get_file_metadata(created_file_document)
        )
        return file_document_response

    def create_one_raw(self, state: State, file_document_creator: FileDocument,
                       file_data: Optional[bytes] = None) -> FileDocument:
        created_file_document: FileDocument = self.file_document_repository.create_one(
            session=state.session,
            file_document_creator=file_document_creator,
            file_data=file_data
        )
        return created_file_document

    async def patch_one_by_id_with_authorization(self, state: State, id: UUID,
                                                 body: PatchOneBody) -> FileDocumentResponse:
        document_patcher: Document = Document(
            id=id,
            name=body.name,
            description=body.description,
            document_type_id=DocumentTypeConstant.FILE,
            account_id=body.account_id
        )
        patched_document: Document = await self.document_management.patch_one_by_id_raw_with_authorization(
            state=state,
            id=id,
            document_patcher=document_patcher
        )
        file_data: Optional[bytes] = None
        file_document_patcher: FileDocument = FileDocument(
            file_name=f"{uuid.uuid4()}_{body.file_name}"
        )
        if body.file_data is not None:
            file_data = await body.file_data.read()
            await body.file_data.close()
            file_document_patcher.file_data_hash = hashlib.sha256(file_data).hexdigest()
        patched_file_document: FileDocument = await self.patch_one_by_id_raw_with_authorization(
            state=state,
            id=id,
            file_document_patcher=file_document_patcher,
            file_data=file_data
        )
        patched_file_document_response: FileDocumentResponse = FileDocumentResponse(
            id=patched_document.id,
            name=patched_document.name,
            description=patched_document.description,
            document_type_id=patched_document.document_type_id,
            account_id=patched_document.account_id,
            file_name=patched_file_document.file_name,
            file_data_hash=patched_file_document.file_data_hash,
            file_metadata=self.get_file_metadata(patched_file_document)
        )
        return patched_file_document_response

    async def patch_one_by_id_raw_with_authorization(self, state: State, id: UUID, file_document_patcher: FileDocument,
                                                     file_data: Optional[bytes] = None) -> FileDocument:
        patched_file_document: FileDocument = await self.file_document_repository.patch_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id,
            file_document_patcher=file_document_patcher,
            file_data=file_data
        )
        return patched_file_document

    async def delete_one_by_id_with_authorization(self, state: State, id: UUID) -> FileDocumentResponse:
        deleted_file_document: FileDocument = await self.file_document_repository.delete_one_by_id_and_account_id(
            session=state.session,
            id=id,
            account_id=state.authorized_session.account_id
        )
        deleted_document: Document = await self.document_management.delete_one_by_id_with_authorization(
            state=state,
            id=id
        )
        deleted_file_document_response: FileDocumentResponse = FileDocumentResponse(
            id=deleted_document.id,
            name=deleted_document.name,
            description=deleted_document.description,
            document_type_id=deleted_document.document_type_id,
            account_id=deleted_document.account_id,
            file_name=deleted_file_document.file_name,
            file_data_hash=deleted_file_document.file_data_hash,
            file_metadata=None
        )
        return deleted_file_document_response
