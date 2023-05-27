from typing import List
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi_utils.cbv import cbv

from app.inners.models.entities.document_process import DocumentProcess
from app.inners.models.value_objects.contracts.requests.managements.document_processes.create_body import \
    CreateBody
from app.inners.models.value_objects.contracts.requests.managements.document_processes.create_one_request import \
    CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.document_processes.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.document_processes.patch_body import \
    PatchBody
from app.inners.models.value_objects.contracts.requests.managements.document_processes.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.document_processes.read_all_request import \
    ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.document_processes.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.use_cases.managements.document_process_management import DocumentProcessManagement

router: APIRouter = APIRouter(tags=["document-processes"])


@cbv(router)
class DocumentProcessController:
    def __init__(self):
        self.document_process_management: DocumentProcessManagement = DocumentProcessManagement()

    @router.get("/document-processes")
    async def read_all(self, request: Request) -> Content[List[DocumentProcess]]:
        request: ReadAllRequest = ReadAllRequest(query_parameter=dict(request.query_params))
        return await self.document_process_management.read_all(request=request)

    @router.get("/document-processes/{id}")
    async def read_one_by_id(self, id: UUID) -> Content[DocumentProcess]:
        request: ReadOneByIdRequest = ReadOneByIdRequest(id=id)
        return await self.document_process_management.read_one_by_id(request)

    @router.post("/document-processes")
    async def create_one(self, body: CreateBody) -> Content[DocumentProcess]:
        request: CreateOneRequest = CreateOneRequest(body=body)
        return await self.document_process_management.create_one(request)

    @router.patch("/document-processes/{id}")
    async def patch_one_by_id(self, id: UUID, body: PatchBody) -> Content[DocumentProcess]:
        request: PatchOneByIdRequest = PatchOneByIdRequest(id=id, body=body)
        return await self.document_process_management.patch_one_by_id(request)

    @router.delete("/document-processes/{id}")
    async def delete_one_by_id(self, id: UUID) -> Content[DocumentProcess]:
        request: DeleteOneByIdRequest = DeleteOneByIdRequest(id=id)
        return await self.document_process_management.delete_one_by_id(request)
