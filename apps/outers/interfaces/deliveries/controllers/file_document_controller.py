from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request, Depends, File, Form, UploadFile
from fastapi_utils.cbv import cbv
from starlette.responses import Response

from apps.inners.models.dtos.contracts.content import Content
from apps.inners.models.dtos.contracts.requests.managements.file_documents.create_one_body import CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.file_documents.patch_one_body import PatchOneBody
from apps.inners.models.dtos.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from apps.inners.models.dtos.contracts.result import Result
from apps.inners.use_cases.managements.file_document_management import FileDocumentManagement
from apps.outers.containers.application_container import ApplicationContainer

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

    @router.get("/documents/files/{id}")
    async def find_one_by_id(self, request: Request, id: UUID) -> Response:
        result: Result[FileDocumentResponse] = await self.file_document_management.find_one_by_id(
            state=request.state,
            id=id
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[FileDocumentResponse](
                message=result.message,
                data=result.data
            ).json()
        )
        return response

    @router.post("/documents/files")
    async def create_one(
            self,
            request: Request,
            document_name: str = Form(...),
            document_description: str = Form(...),
            document_type_id: str = Form(...),
            document_account_id: UUID = Form(...),
            file_name: str = Form(...),
            file_data: UploadFile = File(...)
    ) -> Response:
        body: CreateOneBody = CreateOneBody(
            document_name=document_name,
            document_description=document_description,
            document_type_id=document_type_id,
            document_account_id=document_account_id,
            file_name=file_name,
            file_data=file_data
        )
        result: Result[FileDocumentResponse] = await self.file_document_management.create_one(
            state=request.state,
            body=body,
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[FileDocumentResponse](
                message=result.message,
                data=result.data
            ).json()
        )
        return response

    @router.patch("/documents/files/{id}")
    async def patch_one_by_id(
            self,
            request: Request,
            id: UUID,
            document_name: str = Form(...),
            document_description: str = Form(...),
            document_type_id: str = Form(...),
            document_account_id: UUID = Form(...),
            file_name: str = Form(...),
            file_data: UploadFile = File(...)
    ) -> Response:
        body: PatchOneBody = PatchOneBody(
            document_name=document_name,
            document_description=document_description,
            document_type_id=document_type_id,
            document_account_id=document_account_id,
            file_name=file_name,
            file_data=file_data
        )
        result: Result[FileDocumentResponse] = await self.file_document_management.patch_one_by_id(
            state=request.state,
            id=id,
            body=body
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[FileDocumentResponse](
                message=result.message,
                data=result.data
            ).json()
        )
        return response

    @router.delete("/documents/files/{id}")
    async def delete_one_by_id(self, request: Request, id: UUID) -> Response:
        result: Result[FileDocumentResponse] = await self.file_document_management.delete_one_by_id(
            state=request.state,
            id=id
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[FileDocumentResponse](
                message=result.message,
                data=result.data
            ).json()
        )
        return response
