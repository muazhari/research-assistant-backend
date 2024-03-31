from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request, Depends, File, Form, UploadFile
from fastapi_utils.cbv import cbv
from starlette import status
from starlette.responses import Response

from apps.inners.models.dtos.contracts.content import Content
from apps.inners.models.dtos.contracts.requests.managements.file_documents.create_one_body import CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.file_documents.patch_one_body import PatchOneBody
from apps.inners.models.dtos.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from apps.inners.models.dtos.contracts.result import Result
from apps.inners.use_cases.managements.file_document_management import FileDocumentManagement
from apps.outers.containers.application_container import ApplicationContainer
from apps.outers.exceptions import repository_exception

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
        content: Content[FileDocumentResponse] = Content[FileDocumentResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.find_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: FileDocumentResponse = await self.file_document_management.find_one_by_id(
                state=request.state,
                id=id
            )
            content.status_code = status.HTTP_200_OK
            content.message = f"{self.__class__.__name__}.{self.find_one_by_id.__name__}: Succeed."
            content.data = data
        except repository_exception.NotFound as exception:
            content.status_code = status.HTTP_404_NOT_FOUND
            content.message += f" {exception.__class__.__name__}."

        return content.to_response()

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
        content: Content[FileDocumentResponse] = Content[FileDocumentResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.create_one.__name__}: Failed.",
            data=None
        )
        try:
            data: FileDocumentResponse = await self.file_document_management.create_one(
                state=request.state,
                body=body
            )
            content.status_code = status.HTTP_201_CREATED
            content.message = f"{self.__class__.__name__}.{self.create_one.__name__}: Succeed."
            content.data = data
        except repository_exception.IntegrityError as exception:
            content.status_code = status.HTTP_409_CONFLICT
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."

        return content.to_response()

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
        content: Content[FileDocumentResponse] = Content[FileDocumentResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.patch_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: FileDocumentResponse = await self.file_document_management.patch_one_by_id(
                state=request.state,
                id=id,
                body=body
            )
            content.status_code = status.HTTP_200_OK
            content.message = f"{self.__class__.__name__}.{self.patch_one_by_id.__name__}: Succeed."
            content.data = data
        except repository_exception.NotFound as exception:
            content.status_code = status.HTTP_404_NOT_FOUND
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."

        return content.to_response()

    @router.delete("/documents/files/{id}")
    async def delete_one_by_id(self, request: Request, id: UUID) -> Response:
        content: Content[Result] = Content[Result](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.delete_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: FileDocumentResponse = await self.file_document_management.delete_one_by_id(
                state=request.state,
                id=id
            )
            content.status_code = status.HTTP_200_OK
            content.message = f"{self.__class__.__name__}.{self.delete_one_by_id.__name__}: Succeed."
            content.data = data
        except repository_exception.NotFound as exception:
            content.status_code = status.HTTP_404_NOT_FOUND
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."

        return content.to_response()
