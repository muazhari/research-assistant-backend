from typing import List
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request, Depends
from fastapi_utils.cbv import cbv

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
from app.inners.models.value_objects.contracts.responses.managements.documents.web_document_response import \
    WebDocumentResponse
from app.inners.use_cases.managements.web_document_management import WebDocumentManagement
from app.outers.containers.application_container import ApplicationContainer

router: APIRouter = APIRouter(tags=["web-documents"])


@cbv(router)
class WebDocumentController:

    @inject
    def __init__(
            self,
            web_document_management: WebDocumentManagement = Depends(
                Provide[ApplicationContainer.use_cases.managements.web_document]
            )
    ) -> None:
        self.web_document_management: WebDocumentManagement = web_document_management

    @router.get("/documents/webs")
    async def read_all(self, request: Request) -> Content[List[WebDocumentResponse]]:
        request: ReadAllRequest = ReadAllRequest(query_parameter=dict(request.query_params))
        return await self.web_document_management.read_all(request=request)

    @router.get("/documents/webs/{id}")
    async def read_one_by_id(self, id: UUID) -> Content[WebDocumentResponse]:
        request: ReadOneByIdRequest = ReadOneByIdRequest(id=id)
        return await self.web_document_management.read_one_by_id(request)

    @router.post("/documents/webs")
    async def create_one(self, body: CreateBody) -> Content[WebDocumentResponse]:
        request: CreateOneRequest = CreateOneRequest(body=body)
        return await self.web_document_management.create_one(request)

    @router.patch("/documents/webs/{id}")
    async def patch_one_by_id(self, id: UUID, body: PatchBody) -> Content[WebDocumentResponse]:
        request: PatchOneByIdRequest = PatchOneByIdRequest(id=id, body=body)
        return await self.web_document_management.patch_one_by_id(request)

    @router.delete("/documents/webs/{id}")
    async def delete_one_by_id(self, id: UUID) -> Content[WebDocumentResponse]:
        request: DeleteOneByIdRequest = DeleteOneByIdRequest(id=id)
        return await self.web_document_management.delete_one_by_id(request)
