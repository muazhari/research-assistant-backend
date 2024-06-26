from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from apps.inners.exceptions import repository_exception
from apps.inners.models.daos.document_type import DocumentType
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.managements.document_types.patch_one_body import \
    PatchOneBody
from apps.inners.use_cases.managements.document_type_management import DocumentTypeManagement


class DocumentTypeController:

    def __init__(
            self,
            document_type_management: DocumentTypeManagement
    ) -> None:
        self.router = APIRouter(
            tags=["document-types"],
            prefix="/document-types"
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.find_one_by_id,
            methods=["GET"]
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.patch_one_by_id,
            methods=["PATCH"]
        )
        self.document_type_management: DocumentTypeManagement = document_type_management

    async def find_one_by_id(self, request: Request, id: str) -> Response:
        content: Content[DocumentType] = Content[DocumentType](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.find_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: DocumentType = await self.document_type_management.find_one_by_id(
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

    async def patch_one_by_id(self, request: Request, id: str, body: PatchOneBody) -> Response:
        content: Content[DocumentType] = Content[DocumentType](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.patch_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: DocumentType = await self.document_type_management.patch_one_by_id(
                state=request.state,
                id=id,
                body=body
            )
            content.status_code = status.HTTP_200_OK
            content.message = f"{self.__class__.__name__}.{self.patch_one_by_id.__name__}: Succeed."
            content.data = data
        except repository_exception.NotFound as exception:
            content.status_code = status.HTTP_404_NOT_FOUND
            content.message += f" {exception.__class__.__name__}."
        except repository_exception.IntegrityError as exception:
            content.status_code = status.HTTP_409_CONFLICT
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."

        return content.to_response()
