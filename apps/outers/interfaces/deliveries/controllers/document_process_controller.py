from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from apps.inners.models.daos.document_process import DocumentProcess
from apps.inners.models.dtos.contracts.content import Content
from apps.inners.models.dtos.contracts.requests.managements.document_processes.create_one_body import \
    CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.document_processes.patch_one_body import \
    PatchOneBody
from apps.inners.models.dtos.contracts.result import Result
from apps.inners.use_cases.managements.document_process_management import DocumentProcessManagement
from apps.outers.containers.application_container import ApplicationContainer
from apps.outers.exceptions import repository_exception

router: APIRouter = APIRouter(tags=["document-processes"])


@cbv(router)
class DocumentProcessController:

    @inject
    def __init__(
            self,
            document_process_management: DocumentProcessManagement = Depends(
                Provide[ApplicationContainer.use_cases.managements.document_process]
            )
    ) -> None:
        self.document_process_management: DocumentProcessManagement = document_process_management

    @router.get("/document-processes/{id}")
    async def find_one_by_id(self, request: Request, id: UUID) -> Response:
        content: Content[DocumentProcess] = Content[DocumentProcess](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.find_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: DocumentProcess = await self.document_process_management.find_one_by_id(
                state=request.state,
                id=id
            )
            content.status_code = status.HTTP_200_OK
            content.message = f"{self.__class__.__name__}.{self.find_one_by_id.__name__}: Succeed."
            content.data = data
        except repository_exception.NotFound as exception:
            content.status_code = status.HTTP_404_NOT_FOUND
            content.message += f" {exception.__class__.__name__}."
        response: Response = Response(
            status_code=content.status_code,
            content=content.json()
        )
        return response

    @router.post("/document-processes")
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

    @router.patch("/document-processes/{id}")
    async def patch_one_by_id(self, request: Request, id: UUID, body: PatchOneBody) -> Response:
        content: Content[DocumentProcess] = Content[DocumentProcess](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.patch_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: DocumentProcess = await self.document_process_management.patch_one_by_id(
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

    @router.delete("/document-processes/{id}")
    async def delete_one_by_id(self, request: Request, id: UUID) -> Response:
        content: Content[Result] = Content[Result](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.delete_one_by_id.__name__}: Failed.",
            data=None
        )
        try:
            data: DocumentProcess = await self.document_process_management.delete_one_by_id(
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
