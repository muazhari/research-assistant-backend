from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Request, File, Form, UploadFile
from starlette import status
from starlette.responses import Response

from apps.inners.exceptions import repository_exception
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.managements.file_documents.create_one_body import CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.file_documents.patch_one_body import PatchOneBody
from apps.inners.models.dtos.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from apps.inners.use_cases.managements.file_document_management import FileDocumentManagement


class FileDocumentController:

    def __init__(
            self,
            file_document_management: FileDocumentManagement
    ) -> None:
        self.router: APIRouter = APIRouter(
            tags=["document-files"],
            prefix="/document-files"
        )
        self.router.add_api_route(
            path="",
            endpoint=self.find_many_with_pagination,
            methods=["GET"]
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.find_one_by_id,
            methods=["GET"]
        )
        self.router.add_api_route(
            path="",
            endpoint=self.create_one,
            methods=["POST"]
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.patch_one_by_id,
            methods=["PATCH"]
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.delete_one_by_id,
            methods=["DELETE"]
        )

        self.file_document_management = file_document_management

    async def find_many_with_pagination(self, request: Request, page_position: int = 1,
                                        page_size: int = 10) -> Response:
        content: Content[List[FileDocumentResponse]] = Content[List[FileDocumentResponse]](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.find_many_with_pagination.__name__}: Failed.",
            data=None
        )

        data: List[
            FileDocumentResponse
        ] = await self.file_document_management.find_many_with_authorization_and_pagination(
            state=request.state,
            page_position=page_position,
            page_size=page_size
        )
        content.status_code = status.HTTP_200_OK
        content.message = f"{self.__class__.__name__}.{self.find_many_with_pagination.__name__}: Succeed."
        content.data = data

        return content.to_response()

    async def find_one_by_id(self, request: Request, id: UUID) -> Response:
        content: Content[FileDocumentResponse] = Content[FileDocumentResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.find_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: FileDocumentResponse = await self.file_document_management.find_one_by_id_with_authorization(
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

    async def create_one(
            self,
            request: Request,
            name: str = Form(default=""),
            description: str = Form(default=""),
            account_id: UUID = Form(...),
            file_name: str = Form(default=""),
            file_data: UploadFile = File(...)
    ) -> Response:
        body: CreateOneBody = CreateOneBody(
            name=name,
            description=description,
            account_id=account_id,
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

    async def patch_one_by_id(
            self,
            request: Request,
            id: UUID,
            name: str = Form(default=""),
            description: str = Form(default=""),
            account_id: UUID = Form(...),
            file_name: str = Form(default=""),
            file_data: Optional[UploadFile] = File(default=None)
    ) -> Response:
        body: PatchOneBody = PatchOneBody(
            name=name,
            description=description,
            account_id=account_id,
            file_name=file_name,
            file_data=file_data
        )
        content: Content[FileDocumentResponse] = Content[FileDocumentResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.patch_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: FileDocumentResponse = await self.file_document_management.patch_one_by_id_with_authorization(
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

    async def delete_one_by_id(self, request: Request, id: UUID) -> Response:
        content: Content[FileDocumentResponse] = Content[FileDocumentResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.delete_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: FileDocumentResponse = await self.file_document_management.delete_one_by_id_with_authorization(
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
