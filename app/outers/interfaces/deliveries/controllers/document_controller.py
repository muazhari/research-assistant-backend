from typing import List
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi_utils.cbv import cbv

from app.inners.models.entities.document import Document
from app.inners.models.value_objects.contracts.requests.managements.documents.create_body import \
    CreateBody
from app.inners.models.value_objects.contracts.requests.managements.documents.create_one_request import \
    CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.documents.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.documents.patch_body import \
    PatchBody
from app.inners.models.value_objects.contracts.requests.managements.documents.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.documents.read_all_request import ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.documents.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.use_cases.managements.document_management import DocumentManagement

router: APIRouter = APIRouter(tags=["documents"])


@cbv(router)
class DocumentController:
    def __init__(self):
        self.document_management: DocumentManagement = DocumentManagement()

    @router.get("/documents")
    async def read_all(self, request: Request) -> Content[List[Document]]:
        request: ReadAllRequest = ReadAllRequest(query_parameter=dict(request.query_params))
        return await self.document_management.read_all(request=request)

    @router.get("/documents/{id}")
    async def read_one_by_id(self, id: UUID) -> Content[Document]:
        request: ReadOneByIdRequest = ReadOneByIdRequest(id=id)
        return await self.document_management.read_one_by_id(request)

    @router.post("/documents")
    async def create_one(self, body: CreateBody) -> Content[Document]:
        request: CreateOneRequest = CreateOneRequest(body=body)
        return await self.document_management.create_one(request)

    @router.patch("/documents/{id}")
    async def patch_one_by_id(self, id: UUID, body: PatchBody) -> Content[Document]:
        request: PatchOneByIdRequest = PatchOneByIdRequest(id=id, body=body)
        return await self.document_management.patch_one_by_id(request)

    @router.delete("/documents/{id}")
    async def delete_one_by_id(self, id: UUID) -> Content[Document]:
        request: DeleteOneByIdRequest = DeleteOneByIdRequest(id=id)
        return await self.document_management.delete_one_by_id(request)
