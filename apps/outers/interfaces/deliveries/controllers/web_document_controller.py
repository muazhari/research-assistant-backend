from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request, Depends
from fastapi_utils.cbv import cbv
from starlette import status
from starlette.responses import Response

from apps.inners.models.dtos.contracts.content import Content
from apps.inners.models.dtos.contracts.requests.managements.web_documents.create_one_body import \
    CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.web_documents.patch_one_body import \
    PatchOneBody
from apps.inners.models.dtos.contracts.responses.managements.documents.web_document_response import \
    WebDocumentResponse
from apps.inners.models.dtos.contracts.result import Result
from apps.inners.use_cases.managements.web_document_management import WebDocumentManagement
from apps.outers.containers.application_container import ApplicationContainer
from apps.outers.exceptions import repository_exception
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request, Depends
from fastapi_utils.cbv import cbv
from starlette import status
from starlette.responses import Response

from apps.inners.models.dtos.contracts.content import Content
from apps.inners.models.dtos.contracts.requests.managements.web_documents.create_one_body import \
    CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.web_documents.patch_one_body import \
    PatchOneBody
from apps.inners.models.dtos.contracts.responses.managements.documents.web_document_response import \
    WebDocumentResponse
from apps.inners.models.dtos.contracts.result import Result
from apps.inners.use_cases.managements.web_document_management import WebDocumentManagement
from apps.outers.containers.application_container import ApplicationContainer
from apps.outers.exceptions import repository_exception

router: APIRouter = APIRouter(tags=["web-documents"])


@cbv(router)
class WebDocumentController:

    @inject
    def __init__(
            self,
            web_document_management: WebDocumentManagement = Depends(
                Provide[ApplicationContainer.use_cases.managements.web_document]
            )
    ) -> None:
        self.web_document_management = web_document_management

    @router.get("/documents/webs/{id}")
    async def find_one_by_id(self, request: Request, id: UUID) -> Response:
        content: Content[WebDocumentResponse] = Content[WebDocumentResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.find_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: WebDocumentResponse = await self.web_document_management.find_one_by_id(
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

    @router.post("/documents/webs")
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

    @router.patch("/documents/webs/{id}")
    async def patch_one_by_id(self, request: Request, id: UUID, body: PatchOneBody) -> Response:
        content: Content[WebDocumentResponse] = Content[WebDocumentResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.patch_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: WebDocumentResponse = await self.web_document_management.patch_one_by_id(
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

    @router.delete("/documents/webs/{id}")
    async def delete_one_by_id(self, request: Request, id: UUID) -> Response:
        content: Content[Result] = Content[Result](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.delete_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: WebDocumentResponse = await self.web_document_management.delete_one_by_id(
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
