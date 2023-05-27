from typing import List
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi_utils.cbv import cbv

from app.inners.models.entities.web_document import WebDocument
from app.inners.models.value_objects.contracts.requests.managements.web_documents.create_body import \
    CreateBody
from app.inners.models.value_objects.contracts.requests.managements.web_documents.create_one_request import \
    CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.web_documents.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.web_documents.patch_body import \
    PatchBody
from app.inners.models.value_objects.contracts.requests.managements.web_documents.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.web_documents.read_all_request import \
    ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.web_documents.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.use_cases.managements.web_document_management import WebDocumentManagement

router: APIRouter = APIRouter(tags=["web-documents"])


@cbv(router)
class WebDocumentController:
    def __init__(self):
        self.web_document_management: WebDocumentManagement = WebDocumentManagement()

    @router.get("/documents/webs")
    async def read_all(self, request: Request) -> Content[List[WebDocument]]:
        request: ReadAllRequest = ReadAllRequest(query_parameter=dict(request.query_params))
        return await self.web_document_management.read_all(request=request)

    @router.get("/documents/webs/{id}")
    async def read_one_by_id(self, id: UUID) -> Content[WebDocument]:
        request: ReadOneByIdRequest = ReadOneByIdRequest(id=id)
        return await self.web_document_management.read_one_by_id(request)

    @router.post("/documents/webs")
    async def create_one(self, body: CreateBody) -> Content[WebDocument]:
        request: CreateOneRequest = CreateOneRequest(body=body)
        return await self.web_document_management.create_one(request)

    @router.patch("/documents/webs/{id}")
    async def patch_one_by_id(self, id: UUID, body: PatchBody) -> Content[WebDocument]:
        request: PatchOneByIdRequest = PatchOneByIdRequest(id=id, body=body)
        return await self.web_document_management.patch_one_by_id(request)

    @router.delete("/documents/webs/{id}")
    async def delete_one_by_id(self, id: UUID) -> Content[WebDocument]:
        request: DeleteOneByIdRequest = DeleteOneByIdRequest(id=id)
        return await self.web_document_management.delete_one_by_id(request)
