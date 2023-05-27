from typing import List
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi_utils.cbv import cbv

from app.inners.models.entities.document_type import DocumentType
from app.inners.models.value_objects.contracts.requests.managements.document_types.create_body import \
    CreateBody
from app.inners.models.value_objects.contracts.requests.managements.document_types.create_one_request import \
    CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.document_types.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.document_types.patch_body import \
    PatchBody
from app.inners.models.value_objects.contracts.requests.managements.document_types.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.document_types.read_all_request import \
    ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.document_types.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.use_cases.managements.document_type_management import DocumentTypeManagement

router: APIRouter = APIRouter(tags=["document-types"])


@cbv(router)
class DocumentTypeController:
    def __init__(self):
        self.document_type_management: DocumentTypeManagement = DocumentTypeManagement()

    @router.get("/document-types")
    async def read_all(self, request: Request) -> Content[List[DocumentType]]:
        request: ReadAllRequest = ReadAllRequest(query_parameter=dict(request.query_params))
        return await self.document_type_management.read_all(request=request)

    @router.get("/document-types/{id}")
    async def read_one_by_id(self, id: UUID) -> Content[DocumentType]:
        request: ReadOneByIdRequest = ReadOneByIdRequest(id=id)
        return await self.document_type_management.read_one_by_id(request)

    @router.post("/document-types")
    async def create_one(self, body: CreateBody) -> Content[DocumentType]:
        request: CreateOneRequest = CreateOneRequest(body=body)
        return await self.document_type_management.create_one(request)

    @router.patch("/document-types/{id}")
    async def patch_one_by_id(self, id: UUID, body: PatchBody) -> Content[DocumentType]:
        request: PatchOneByIdRequest = PatchOneByIdRequest(id=id, body=body)
        return await self.document_type_management.patch_one_by_id(request)

    @router.delete("/document-types/{id}")
    async def delete_one_by_id(self, id: UUID) -> Content[DocumentType]:
        request: DeleteOneByIdRequest = DeleteOneByIdRequest(id=id)
        return await self.document_type_management.delete_one_by_id(request)
