from typing import List
from uuid import UUID

from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from apps.inners.exceptions import repository_exception
from apps.inners.models.daos.document_process import DocumentProcess
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.managements.document_processes.create_one_body import \
    CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.document_processes.patch_one_body import \
    PatchOneBody
from apps.inners.use_cases.managements.document_process_management import DocumentProcessManagement


class DocumentProcessController:

    def __init__(
            self,
            document_process_management: DocumentProcessManagement
    ) -> None:
        self.router = APIRouter(
            tags=["document-processes"],
            prefix="/document-processes"
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
        self.document_process_management: DocumentProcessManagement = document_process_management

    async def find_many_with_pagination(self, request: Request, page_position: int = 1, page_size: int = 10) -> Response:
        content: Content[List[DocumentProcess]] = Content[List[DocumentProcess]](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.find_many_with_pagination.__name__}: Failed.",
            data=None
        )

        data: List[
            DocumentProcess
        ] = await self.document_process_management.find_many_with_authorization_and_pagination(
            state=request.state,
            page_position=page_position,
            page_size=page_size
        )
        content.status_code = status.HTTP_200_OK
        content.message = f"{self.__class__.__name__}.{self.find_many_with_pagination.__name__}: Succeed."
        content.data = data

        return content.to_response()

    async def find_one_by_id(self, request: Request, id: UUID) -> Response:
        content: Content[DocumentProcess] = Content[DocumentProcess](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.find_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: DocumentProcess = await self.document_process_management.find_one_by_id_with_authorization(
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

    async def create_one(self, request: Request, body: CreateOneBody) -> Response:
        content: Content[DocumentProcess] = Content[DocumentProcess](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.create_one.__name__}: Failed.",
            data=None
        )
        try:
            data: DocumentProcess = await self.document_process_management.create_one(
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
        content: Content[DocumentProcess] = Content[DocumentProcess](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.patch_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: DocumentProcess = await self.document_process_management.patch_one_by_id_with_authorization(
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
        content: Content[DocumentProcess] = Content[DocumentProcess](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.delete_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: DocumentProcess = await self.document_process_management.delete_one_by_id_with_authorization(
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
