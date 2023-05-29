import asyncio
import uuid
from typing import List

from app.inners.models.entities.document import Document
from app.inners.models.entities.web_document import WebDocument
from app.inners.models.value_objects.contracts.requests.managements.web_documents.create_one_request import \
    CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.web_documents.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.web_documents.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.web_documents.read_all_request import \
    ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.web_documents.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.managements.documents.web_document_response import \
    WebDocumentResponse
from app.outers.repositories.document_repository import DocumentRepository
from app.outers.repositories.web_document_repository import WebDocumentRepository
from app.outers.utilities.management_utility import ManagementUtility


class WebDocumentManagement:
    def __init__(self):
        self.management_utility: ManagementUtility = ManagementUtility()
        self.document_repository: DocumentRepository = DocumentRepository()
        self.web_document_repository: WebDocumentRepository = WebDocumentRepository()

    async def read_all(self, request: ReadAllRequest) -> Content[List[WebDocumentResponse]]:
        try:
            found_web_documents: List[WebDocument] = await self.web_document_repository.read_all()
            found_document_coroutines = [
                self.document_repository.read_one_by_id(web_document.document_id)
                for web_document in found_web_documents
            ]
            found_documents: List[Document] = await asyncio.gather(*found_document_coroutines)

            found_entities: List[WebDocumentResponse] = [
                WebDocumentResponse(
                    id=document.id,
                    name=document.name,
                    description=document.description,
                    document_type_id=document.document_type_id,
                    account_id=document.account_id,
                    web_url=web_document.web_url,
                )
                for document, web_document in zip(found_documents, found_web_documents)
            ]

            if len(request.query_parameter.keys()) > 0:
                found_entities = list(
                    filter(
                        lambda entity: self.management_utility.filter(request.query_parameter, entity),
                        found_entities
                    )
                )

            content: Content[List[WebDocumentResponse]] = Content(
                message="WebDocument read all succeed.",
                data=found_entities,
            )
        except Exception as exception:
            content: Content[List[WebDocumentResponse]] = Content(
                message=f"WebDocument read all failed: {exception}",
                data=None,
            )
        return content

    async def read_one_by_id(self, request: ReadOneByIdRequest) -> Content[WebDocumentResponse]:
        try:
            found_web_document: WebDocument = await self.web_document_repository.read_one_by_id(
                id=request.id
            )
            found_document: Document = await self.document_repository.read_one_by_id(
                id=found_web_document.document_id
            )

            content: Content[WebDocumentResponse] = Content(
                message="WebDocument read one by id succeed.",
                data=WebDocumentResponse(
                    id=found_document.id,
                    name=found_document.name,
                    description=found_document.description,
                    document_type_id=found_document.document_type_id,
                    account_id=found_document.account_id,
                    web_url=found_web_document.web_url,
                )
            )
        except Exception as exception:
            content: Content[WebDocumentResponse] = Content(
                message=f"WebDocument read one by id failed: {exception}",
                data=None,
            )
        return content

    async def create_one(self, request: CreateOneRequest) -> Content[WebDocumentResponse]:
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

            created_web_document: WebDocument = await self.web_document_repository.create_one(
                entity=WebDocument(
                    id=uuid.uuid4(),
                    document_id=created_document.id,
                    web_url=request.body.web_url,
                )
            )

            content: Content[WebDocumentResponse] = Content(
                data=WebDocumentResponse(
                    id=created_document.id,
                    name=created_document.name,
                    description=created_document.description,
                    document_type_id=created_document.document_type_id,
                    account_id=created_document.account_id,
                    web_url=created_web_document.web_url,
                ),
                message="WebDocument create one succeed."
            )
        except Exception as exception:
            content: Content[WebDocumentResponse] = Content(
                data=None,
                message=f"WebDocument create one failed: {exception}"
            )
        return content

    async def patch_one_by_id(self, request: PatchOneByIdRequest) -> Content[WebDocumentResponse]:
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

            found_web_document: WebDocument = await self.web_document_repository.read_one_by_document_id(
                document_id=patched_document.id
            )
            patched_web_document: WebDocument = await self.web_document_repository.patch_one_by_id(
                id=found_web_document.id,
                entity=WebDocument(
                    id=found_web_document.id,
                    document_id=found_web_document.document_id,
                    web_url=request.body.web_url,
                )
            )

            content: Content[WebDocumentResponse] = Content(
                data=WebDocumentResponse(
                    id=patched_document.id,
                    name=patched_document.name,
                    description=patched_document.description,
                    document_type_id=patched_document.document_type_id,
                    account_id=patched_document.account_id,
                    web_url=patched_web_document.web_url,
                ),
                message="WebDocument patch one by id succeed."
            )
        except Exception as exception:
            content: Content[WebDocumentResponse] = Content(
                data=None,
                message=f"WebDocument patch one by id failed: {exception}"
            )
        return content

    async def delete_one_by_id(self, request: DeleteOneByIdRequest) -> Content[WebDocumentResponse]:
        try:
            deleted_web_document: WebDocument = await self.web_document_repository.delete_one_by_document_id(
                document_id=request.id
            )

            deleted_document: Document = await self.document_repository.delete_one_by_id(
                id=deleted_web_document.document_id
            )

            content: Content[WebDocumentResponse] = Content(
                message="WebDocument delete one by id succeed.",
                data=WebDocumentResponse(
                    id=deleted_document.id,
                    name=deleted_document.name,
                    description=deleted_document.description,
                    document_type_id=deleted_document.document_type_id,
                    account_id=deleted_document.account_id,
                    web_url=deleted_web_document.web_url,
                ),
            )
        except Exception as exception:
            content: Content[WebDocumentResponse] = Content(
                message=f"WebDocument delete one by id failed: {exception}",
                data=None,
            )
        return content
