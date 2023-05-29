import asyncio
import uuid
from typing import List

from app.inners.models.entities.document import Document
from app.inners.models.entities.text_document import TextDocument
from app.inners.models.value_objects.contracts.requests.managements.text_documents.create_one_request import \
    CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.text_documents.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.text_documents.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.text_documents.read_all_request import \
    ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.text_documents.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.managements.documents.text_document_response import \
    TextDocumentResponse
from app.outers.repositories.document_repository import DocumentRepository
from app.outers.repositories.text_document_repository import TextDocumentRepository
from app.outers.utilities.management_utility import ManagementUtility


class TextDocumentManagement:
    def __init__(self):
        self.management_utility: ManagementUtility = ManagementUtility()
        self.document_repository: DocumentRepository = DocumentRepository()
        self.text_document_repository: TextDocumentRepository = TextDocumentRepository()

    async def read_all(self, request: ReadAllRequest) -> Content[List[TextDocumentResponse]]:
        try:
            found_text_documents: List[TextDocument] = await self.text_document_repository.read_all()
            found_document_coroutines = [
                self.document_repository.read_one_by_id(text_document.document_id)
                for text_document in found_text_documents
            ]
            found_documents: List[Document] = await asyncio.gather(*found_document_coroutines)

            found_entities: List[TextDocumentResponse] = [
                TextDocumentResponse(
                    id=document.id,
                    name=document.name,
                    description=document.description,
                    document_type_id=document.document_type_id,
                    account_id=document.account_id,
                    text_content=text_document.text_content,
                )
                for document, text_document in zip(found_documents, found_text_documents)
            ]

            if len(request.query_parameter.keys()) > 0:
                found_entities = list(
                    filter(
                        lambda entity: self.management_utility.filter(request.query_parameter, entity),
                        found_entities
                    )
                )

            content: Content[List[TextDocumentResponse]] = Content(
                message="TextDocument read all succeed.",
                data=found_entities,
            )
        except Exception as exception:
            content: Content[List[TextDocumentResponse]] = Content(
                message=f"TextDocument read all failed: {exception}",
                data=None,
            )
        return content

    async def read_one_by_id(self, request: ReadOneByIdRequest) -> Content[TextDocumentResponse]:
        try:
            found_text_document: TextDocument = await self.text_document_repository.read_one_by_id(
                id=request.id
            )
            found_document: Document = await self.document_repository.read_one_by_id(
                id=found_text_document.document_id
            )

            content: Content[TextDocumentResponse] = Content(
                message="TextDocument read one by id succeed.",
                data=TextDocumentResponse(
                    id=found_document.id,
                    name=found_document.name,
                    description=found_document.description,
                    document_type_id=found_document.document_type_id,
                    account_id=found_document.account_id,
                    text_content=found_text_document.text_content,
                )
            )
        except Exception as exception:
            content: Content[TextDocumentResponse] = Content(
                message=f"TextDocument read one by id failed: {exception}",
                data=None,
            )
        return content

    async def create_one(self, request: CreateOneRequest) -> Content[TextDocumentResponse]:
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

            created_text_document: TextDocument = await self.text_document_repository.create_one(
                entity=TextDocument(
                    id=uuid.uuid4(),
                    document_id=created_document.id,
                    text_content=request.body.text_content,
                )
            )

            content: Content[TextDocumentResponse] = Content(
                data=TextDocumentResponse(
                    id=created_document.id,
                    name=created_document.name,
                    description=created_document.description,
                    document_type_id=created_document.document_type_id,
                    account_id=created_document.account_id,
                    text_content=created_text_document.text_content,
                ),
                message="TextDocument create one succeed."
            )
        except Exception as exception:
            content: Content[TextDocumentResponse] = Content(
                data=None,
                message=f"TextDocument create one failed: {exception}"
            )
        return content

    async def patch_one_by_id(self, request: PatchOneByIdRequest) -> Content[TextDocumentResponse]:
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

            found_text_document: TextDocument = await self.text_document_repository.read_one_by_document_id(
                document_id=patched_document.id
            )
            patched_text_document: TextDocument = await self.text_document_repository.patch_one_by_id(
                id=found_text_document.id,
                entity=TextDocument(
                    id=found_text_document.id,
                    document_id=found_text_document.document_id,
                    text_content=request.body.text_content,
                )
            )

            content: Content[TextDocumentResponse] = Content(
                data=TextDocumentResponse(
                    id=patched_document.id,
                    name=patched_document.name,
                    description=patched_document.description,
                    document_type_id=patched_document.document_type_id,
                    account_id=patched_document.account_id,
                    text_content=patched_text_document.text_content,
                ),
                message="TextDocument patch one by id succeed."
            )
        except Exception as exception:
            content: Content[TextDocumentResponse] = Content(
                data=None,
                message=f"TextDocument patch one by id failed: {exception}"
            )
        return content

    async def delete_one_by_id(self, request: DeleteOneByIdRequest) -> Content[TextDocumentResponse]:
        try:
            deleted_text_document: TextDocument = await self.text_document_repository.delete_one_by_document_id(
                document_id=request.id
            )

            deleted_document: Document = await self.document_repository.delete_one_by_id(
                id=deleted_text_document.document_id
            )

            content: Content[TextDocumentResponse] = Content(
                message="TextDocument delete one by id succeed.",
                data=TextDocumentResponse(
                    id=deleted_document.id,
                    name=deleted_document.name,
                    description=deleted_document.description,
                    document_type_id=deleted_document.document_type_id,
                    account_id=deleted_document.account_id,
                    text_content=deleted_text_document.text_content,
                ),
            )
        except Exception as exception:
            content: Content[TextDocumentResponse] = Content(
                message=f"TextDocument delete one by id failed: {exception}",
                data=None,
            )
        return content
