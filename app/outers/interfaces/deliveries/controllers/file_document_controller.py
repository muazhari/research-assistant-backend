from typing import List
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi_utils.cbv import cbv

from app.inners.models.entities.file_document import FileDocument
from app.inners.models.value_objects.contracts.requests.managements.file_documents.create_body import \
    CreateBody
from app.inners.models.value_objects.contracts.requests.managements.file_documents.create_one_request import \
    CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.file_documents.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.file_documents.patch_body import \
    PatchBody
from app.inners.models.value_objects.contracts.requests.managements.file_documents.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.file_documents.read_all_request import \
    ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.file_documents.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.use_cases.managements.file_document_management import FileDocumentManagement

router: APIRouter = APIRouter(tags=["file-documents"])


@cbv(router)
class FileDocumentController:
    def __init__(self):
        self.file_document_management: FileDocumentManagement = FileDocumentManagement()

    @router.get("/documents/files")
    async def read_all(self, request: Request) -> Content[List[FileDocument]]:
        request: ReadAllRequest = ReadAllRequest(query_parameter=dict(request.query_params))
        return await self.file_document_management.read_all(request=request)

    @router.get("/documents/files/{id}")
    async def read_one_by_id(self, id: UUID) -> Content[FileDocument]:
        request: ReadOneByIdRequest = ReadOneByIdRequest(id=id)
        return await self.file_document_management.read_one_by_id(request)

    @router.post("/documents/files")
    async def create_one(self, body: CreateBody) -> Content[FileDocument]:
        request: CreateOneRequest = CreateOneRequest(body=body)
        return await self.file_document_management.create_one(request)

    @router.patch("/documents/files/{id}")
    async def patch_one_by_id(self, id: UUID, body: PatchBody) -> Content[FileDocument]:
        request: PatchOneByIdRequest = PatchOneByIdRequest(id=id, body=body)
        return await self.file_document_management.patch_one_by_id(request)

    @router.delete("/documents/files/{id}")
    async def delete_one_by_id(self, id: UUID) -> Content[FileDocument]:
        request: DeleteOneByIdRequest = DeleteOneByIdRequest(id=id)
        return await self.file_document_management.delete_one_by_id(request)
