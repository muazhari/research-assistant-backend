from typing import List
from uuid import UUID

from fastapi import APIRouter, Request
from starlette import status
from starlette.responses import Response

from apps.inners.exceptions import repository_exception
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.managements.web_documents.create_one_body import \
    CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.web_documents.patch_one_body import \
    PatchOneBody
from apps.inners.models.dtos.contracts.responses.managements.documents.web_document_response import \
    WebDocumentResponse
from apps.inners.use_cases.managements.web_document_management import WebDocumentManagement


class WebDocumentController:

    def __init__(
            self,
            web_document_management: WebDocumentManagement
    ) -> None:
        self.router: APIRouter = APIRouter(
            tags=["document-webs"],
            prefix="/document-webs"
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
        self.web_document_management = web_document_management

    async def find_many_with_pagination(self, request: Request) -> Response:
        content: Content[List[WebDocumentResponse]] = Content[List[WebDocumentResponse]](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.find_many_with_pagination.__name__}: Failed.",
            data=None
        )
        try:
            page_number: int = int(request.query_params.get("page_number", 1))
            page_size: int = int(request.query_params.get("page_size", 10))
        except ValueError:
            content.status_code = status.HTTP_400_BAD_REQUEST
            content.message += f" {self.__class__.__name__}.{self.find_many_with_pagination.__name__}: page_number and page_size must be integer."
            return content.to_response()

        try:
            data: List[
                WebDocumentResponse] = await self.web_document_management.find_many_with_authorization_and_pagination(
                state=request.state,
                page_number=page_number,
                page_size=page_size
            )
            content.status_code = status.HTTP_200_OK
            content.message = f"{self.__class__.__name__}.{self.find_many_with_pagination.__name__}: Succeed."
            content.data = data
        except repository_exception.NotFound as exception:
            content.status_code = status.HTTP_404_NOT_FOUND
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."

        return content.to_response()

    async def find_one_by_id(self, request: Request, id: UUID) -> Response:
        content: Content[WebDocumentResponse] = Content[WebDocumentResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.find_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: WebDocumentResponse = await self.web_document_management.find_one_by_id_with_authorization(
                state=request.state,
                id=id
            )
            content.status_code = status.HTTP_200_OK
            content.message = f"{self.__class__.__name__}.{self.find_one_by_id.__name__}: Succeed."
            content.data = data
        except repository_exception.NotFound as exception:
            content.status_code = status.HTTP_404_NOT_FOUND
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."

        return content.to_response()

    async def create_one(self, request: Request, body: CreateOneBody) -> Response:
        content: Content[WebDocumentResponse] = Content[WebDocumentResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.create_one.__name__}: Failed.",
            data=None
        )
        try:
            data: WebDocumentResponse = await self.web_document_management.create_one(
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

    async def patch_one_by_id(self, request: Request, id: UUID, body: PatchOneBody) -> Response:
        content: Content[WebDocumentResponse] = Content[WebDocumentResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.patch_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: WebDocumentResponse = await self.web_document_management.patch_one_by_id_with_authorization(
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
        content: Content[WebDocumentResponse] = Content[WebDocumentResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.delete_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: WebDocumentResponse = await self.web_document_management.delete_one_by_id_with_authorization(
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
