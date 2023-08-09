from typing import List
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request, Depends
from fastapi_utils.cbv import cbv

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
from app.inners.models.value_objects.contracts.responses.managements.documents.file_document_property_response import \
    FileDocumentPropertyResponse
from app.inners.models.value_objects.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from app.inners.use_cases.managements.file_document_management import FileDocumentManagement
from app.outers.containers.application_container import ApplicationContainer

router: APIRouter = APIRouter(tags=["file-documents"])


@cbv(router)
class FileDocumentController:

    @inject
    def __init__(
            self,
            file_document_management: FileDocumentManagement = Depends(
                Provide[ApplicationContainer.use_cases.managements.file_document]
            )
    ) -> None:
        self.file_document_management = file_document_management

    @router.get("/documents/files")
    async def read_all(self, request: Request) -> Content[List[FileDocumentResponse]]:
        request: ReadAllRequest = ReadAllRequest(query_parameter=dict(request.query_params))
        return await self.file_document_management.read_all(request=request)

    @router.get("/documents/files/{id}")
    async def read_one_by_id(self, id: UUID) -> Content[FileDocumentResponse]:
        request: ReadOneByIdRequest = ReadOneByIdRequest(id=id)
        return await self.file_document_management.read_one_by_id(request)

    @router.get("/documents/files/{id}/property")
    async def read_one_property_by_id(self, id: UUID) -> Content[FileDocumentPropertyResponse]:
        request: ReadOneByIdRequest = ReadOneByIdRequest(id=id)
        return await self.file_document_management.read_one_property_by_id(request)

    @router.post("/documents/files")
    async def create_one(self, body: CreateBody) -> Content[FileDocumentResponse]:
        request: CreateOneRequest = CreateOneRequest(body=body)
        return await self.file_document_management.create_one(request)

    @router.patch("/documents/files/{id}")
    async def patch_one_by_id(self, id: UUID, body: PatchBody) -> Content[FileDocumentResponse]:
        request: PatchOneByIdRequest = PatchOneByIdRequest(id=id, body=body)
        return await self.file_document_management.patch_one_by_id(request)

    @router.delete("/documents/files/{id}")
    async def delete_one_by_id(self, id: UUID) -> Content[FileDocumentResponse]:
        request: DeleteOneByIdRequest = DeleteOneByIdRequest(id=id)
        return await self.file_document_management.delete_one_by_id(request)
