from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette.requests import Request
from starlette.responses import Response

from app.inners.models.daos.document_process import DocumentProcess
from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.managements.document_processes.create_one_body import \
    CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.document_processes.patch_one_body import \
    PatchOneBody
from app.inners.models.dtos.contracts.result import Result
from app.inners.use_cases.managements.document_process_management import DocumentProcessManagement
from app.outers.containers.application_container import ApplicationContainer

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
        result: Result[DocumentProcess] = await self.document_process_management.find_one_by_id(
            state=request.state,
            id=id
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[DocumentProcess](
                message=result.message,
                data=result.data
            ).json()
        )
        return response

    @router.post("/document-processes")
    async def create_one(self, request: Request, body: CreateOneBody) -> Response:
        result: Result[DocumentProcess] = await self.document_process_management.create_one(
            state=request.state,
            body=body
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[DocumentProcess](
                message=result.message,
                data=result.data
            ).json()
        )
        return response

    @router.patch("/document-processes/{id}")
    async def patch_one_by_id(self, request: Request, id: UUID, body: PatchOneBody) -> Response:
        result: Result[DocumentProcess] = await self.document_process_management.patch_one_by_id(
            state=request.state,
            id=id,
            body=body
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[DocumentProcess](
                message=result.message,
                data=result.data
            ).json()
        )
        return response

    @router.delete("/document-processes/{id}")
    async def delete_one_by_id(self, request: Request, id: UUID) -> Response:
        result: Result[DocumentProcess] = await self.document_process_management.delete_one_by_id(
            state=request.state,
            id=id
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[DocumentProcess](
                message=result.message,
                data=result.data
            ).json()
        )
        return response
