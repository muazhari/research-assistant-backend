from typing import List
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi_utils.cbv import cbv

from app.inners.models.value_objects.contracts.requests.managements.text_documents.create_body import \
    CreateBody
from app.inners.models.value_objects.contracts.requests.managements.text_documents.create_one_request import \
    CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.text_documents.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.text_documents.patch_body import \
    PatchBody
from app.inners.models.value_objects.contracts.requests.managements.text_documents.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.text_documents.read_all_request import \
    ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.text_documents.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.managements.documents.text_document_response import \
    TextDocumentResponse
from app.inners.use_cases.managements.text_document_management import TextDocumentManagement

router: APIRouter = APIRouter(tags=["text-documents"])


@cbv(router)
class TextDocumentController:
    def __init__(self):
        self.text_document_management: TextDocumentManagement = TextDocumentManagement()

    @router.get("/documents/texts")
    async def read_all(self, request: Request) -> Content[List[TextDocumentResponse]]:
        request: ReadAllRequest = ReadAllRequest(query_parameter=dict(request.query_params))
        return await self.text_document_management.read_all(request=request)

    @router.get("/documents/texts/{id}")
    async def read_one_by_id(self, id: UUID) -> Content[TextDocumentResponse]:
        request: ReadOneByIdRequest = ReadOneByIdRequest(id=id)
        return await self.text_document_management.read_one_by_id(request)

    @router.post("/documents/texts")
    async def create_one(self, body: CreateBody) -> Content[TextDocumentResponse]:
        request: CreateOneRequest = CreateOneRequest(body=body)
        return await self.text_document_management.create_one(request)

    @router.patch("/documents/texts/{id}")
    async def patch_one_by_id(self, id: UUID, body: PatchBody) -> Content[TextDocumentResponse]:
        request: PatchOneByIdRequest = PatchOneByIdRequest(id=id, body=body)
        return await self.text_document_management.patch_one_by_id(request)

    @router.delete("/documents/texts/{id}")
    async def delete_one_by_id(self, id: UUID) -> Content[TextDocumentResponse]:
        request: DeleteOneByIdRequest = DeleteOneByIdRequest(id=id)
        return await self.text_document_management.delete_one_by_id(request)
