from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from apps.inners.models.daos.document import Document
from apps.inners.models.dtos.contracts.content import Content
from apps.inners.models.dtos.contracts.requests.managements.documents.create_one_body import \
    CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.documents.patch_one_body import \
    PatchOneBody
from apps.inners.use_cases.managements.document_management import DocumentManagement
from apps.outers.containers.application_container import ApplicationContainer
from apps.outers.exceptions import repository_exception
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from apps.inners.models.daos.document import Document
from apps.inners.models.dtos.contracts.content import Content
from apps.inners.models.dtos.contracts.requests.managements.documents.create_one_body import \
    CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.documents.patch_one_body import \
    PatchOneBody
from apps.inners.use_cases.managements.document_management import DocumentManagement
from apps.outers.containers.application_container import ApplicationContainer
from apps.outers.exceptions import repository_exception

router: APIRouter = APIRouter(tags=["documents"])


@cbv(router)
class DocumentController:

    @inject
    def __init__(
            self,
            document_management: DocumentManagement = Depends(
                Provide[ApplicationContainer.use_cases.managements.document]
            )
    ) -> None:
        self.document_management: DocumentManagement = document_management

    @router.get("/documents/{id}")
    async def find_one_by_id(self, request: Request, id: UUID) -> Response:
        content: Content[Document] = Content[Document](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.find_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: Document = await self.document_management.find_one_by_id(
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

    @router.post("/documents")
    async def create_one(self, request: Request, body: CreateOneBody) -> Response:
        content: Content[Document] = Content[Document](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.create_one.__name__}: Failed.",
            data=None
        )
        try:
            data: Document = await self.document_management.create_one(
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

    @router.patch("/documents/{id}")
    async def patch_one_by_id(self, request: Request, id: UUID, body: PatchOneBody) -> Response:
        content: Content[Document] = Content[Document](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.patch_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: Document = await self.document_management.patch_one_by_id(
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

    @router.delete("/documents/{id}")
    async def delete_one_by_id(self, request: Request, id: UUID) -> Response:
        content: Content[Document] = Content[Document](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.delete_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: Document = await self.document_management.delete_one_by_id(
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
