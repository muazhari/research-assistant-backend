import asyncio
import uuid
from typing import List

from app.inners.models.entities.document import Document
from app.inners.models.entities.file_document import FileDocument
from app.inners.models.value_objects.contracts.requests.managements.file_documents.create_one_request import \
    CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.file_documents.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.file_documents.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.file_documents.read_all_request import \
    ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.file_documents.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from app.outers.repositories.document_repository import DocumentRepository
from app.outers.repositories.file_document_repository import FileDocumentRepository
from app.outers.utilities.management_utility import ManagementUtility


class FileDocumentManagement:
    def __init__(self):
        self.management_utility: ManagementUtility = ManagementUtility()
        self.document_repository: DocumentRepository = DocumentRepository()
        self.file_document_repository: FileDocumentRepository = FileDocumentRepository()

    async def read_all(self, request: ReadAllRequest) -> Content[List[FileDocumentResponse]]:
        try:
            found_file_documents: List[FileDocument] = await self.file_document_repository.read_all()
            found_document_coroutines = [
                self.document_repository.read_one_by_id(file_document.document_id)
                for file_document in found_file_documents
            ]
            found_documents: List[Document] = await asyncio.gather(*found_document_coroutines)

            found_entities: List[FileDocumentResponse] = [
                FileDocumentResponse(
                    id=document.id,
                    name=document.name,
                    description=document.description,
                    document_type_id=document.document_type_id,
                    account_id=document.account_id,
                    file_name=file_document.file_name,
                    file_extension=file_document.file_extension,
                    file_bytes=file_document.file_bytes,
                )
                for document, file_document in zip(found_documents, found_file_documents)
            ]

            if len(request.query_parameter.keys()) > 0:
                found_entities = list(
                    filter(
                        lambda entity: self.management_utility.filter(request.query_parameter, entity),
                        found_entities
                    )
                )

            content: Content[List[FileDocumentResponse]] = Content(
                message="FileDocument read all succeed.",
                data=found_entities,
            )
        except Exception as exception:
            content: Content[List[FileDocumentResponse]] = Content(
                message=f"FileDocument read all failed: {exception}",
                data=None,
            )
        return content

    async def read_one_by_id(self, request: ReadOneByIdRequest) -> Content[FileDocumentResponse]:
        try:
            found_file_document: FileDocument = await self.file_document_repository.read_one_by_id(
                id=request.id
            )
            found_document: Document = await self.document_repository.read_one_by_id(
                id=found_file_document.document_id
            )

            content: Content[FileDocumentResponse] = Content(
                message="FileDocument read one by id succeed.",
                data=FileDocumentResponse(
                    id=found_document.id,
                    name=found_document.name,
                    description=found_document.description,
                    document_type_id=found_document.document_type_id,
                    account_id=found_document.account_id,
                    file_name=found_file_document.file_name,
                    file_extension=found_file_document.file_extension,
                    file_bytes=found_file_document.file_bytes,
                )
            )
        except Exception as exception:
            content: Content[FileDocumentResponse] = Content(
                message=f"FileDocument read one by id failed: {exception}",
                data=None,
            )
        return content

    async def create_one(self, request: CreateOneRequest) -> Content[FileDocumentResponse]:
        try:
            created_document: Document = await self.document_repository.create_one(
                entity=Document(
                    id=uuid.uuid4(),
                    name=request.body.name,
                    description=request.body.description,
                    document_type_id=request.body.document_type_id,
                    account_id=request.body.account_id,
                )
            )

            created_file_document: FileDocument = await self.file_document_repository.create_one(
                entity=FileDocument(
                    id=uuid.uuid4(),
                    document_id=created_document.id,
                    file_name=request.body.file_name,
                    file_extension=request.body.file_extension,
                    file_bytes=request.body.file_bytes,
                )
            )

            content: Content[FileDocumentResponse] = Content(
                data=FileDocumentResponse(
                    id=created_document.id,
                    name=created_document.name,
                    description=created_document.description,
                    document_type_id=created_document.document_type_id,
                    account_id=created_document.account_id,
                    file_name=created_file_document.file_name,
                    file_extension=created_file_document.file_extension,
                    file_bytes=created_file_document.file_bytes,
                ),
                message="FileDocument create one succeed."
            )
        except Exception as exception:
            content: Content[FileDocumentResponse] = Content(
                data=None,
                message=f"FileDocument create one failed: {exception}"
            )
        return content

    async def patch_one_by_id(self, request: PatchOneByIdRequest) -> Content[FileDocumentResponse]:
        try:
            patched_document: Document = await self.document_repository.patch_one_by_id(
                id=request.id,
                entity=Document(
                    id=request.id,
                    name=request.body.name,
                    description=request.body.description,
                    document_type_id=request.body.document_type_id,
                    account_id=request.body.account_id,
                )
            )

            found_file_document: FileDocument = await self.file_document_repository.read_one_by_document_id(
                document_id=patched_document.id
            )
            patched_file_document: FileDocument = await self.file_document_repository.patch_one_by_id(
                id=found_file_document.id,
                entity=FileDocument(
                    id=found_file_document.id,
                    document_id=found_file_document.document_id,
                    file_name=request.body.file_name,
                    file_extension=request.body.file_extension,
                    file_bytes=request.body.file_bytes,
                )
            )

            content: Content[FileDocumentResponse] = Content(
                data=FileDocumentResponse(
                    id=patched_document.id,
                    name=patched_document.name,
                    description=patched_document.description,
                    document_type_id=patched_document.document_type_id,
                    account_id=patched_document.account_id,
                    file_name=patched_file_document.file_name,
                    file_extension=patched_file_document.file_extension,
                    file_bytes=patched_file_document.file_bytes,
                ),
                message="FileDocument patch one by id succeed."
            )
        except Exception as exception:
            content: Content[FileDocumentResponse] = Content(
                data=None,
                message=f"FileDocument patch one by id failed: {exception}"
            )
        return content

    async def delete_one_by_id(self, request: DeleteOneByIdRequest) -> Content[FileDocumentResponse]:
        try:
            deleted_document: Document = await self.document_repository.delete_one_by_id(
                id=request.id
            )
            deleted_file_document: FileDocument = await self.file_document_repository.delete_one_by_document_id(
                document_id=deleted_document.id
            )

            content: Content[FileDocumentResponse] = Content(
                message="FileDocument delete one by id succeed.",
                data=FileDocumentResponse(
                    id=deleted_document.id,
                    name=deleted_document.name,
                    description=deleted_document.description,
                    document_type_id=deleted_document.document_type_id,
                    account_id=deleted_document.account_id,
                    file_name=deleted_file_document.file_name,
                    file_extension=deleted_file_document.file_extension,
                    file_bytes=deleted_file_document.file_bytes,
                ),
            )
        except Exception as exception:
            content: Content[FileDocumentResponse] = Content(
                message=f"FileDocument delete one by id failed: {exception}",
                data=None,
            )
        return content
