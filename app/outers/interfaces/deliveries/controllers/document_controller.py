from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette.requests import Request
from starlette.responses import Response

from app.inners.models.daos.document import Document
from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.managements.documents.create_one_body import \
    CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.documents.patch_one_body import \
    PatchOneBody
from app.inners.models.dtos.contracts.result import Result
from app.inners.use_cases.managements.document_management import DocumentManagement
from app.outers.containers.application_container import ApplicationContainer

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
        result: Result[Document] = await self.document_management.find_one_by_id(
            state=request.state,
            id=id
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[Document](
                message=result.message,
                data=result.data
            ).json()
        )
        return response

    @router.post("/documents")
    async def create_one(self, request: Request, body: CreateOneBody) -> Response:
        result: Result[Document] = await self.document_management.create_one(
            state=request.state,
            body=body
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[Document](
                message=result.message,
                data=result.data
            ).json()
        )
        return response

    @router.patch("/documents/{id}")
    async def patch_one_by_id(self, request: Request, id: UUID, body: PatchOneBody) -> Response:
        result: Result[Document] = await self.document_management.patch_one_by_id(
            state=request.state,
            id=id,
            body=body
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[Document](
                message=result.message,
                data=result.data
            ).json()
        )
        return response

    @router.delete("/documents/{id}")
    async def delete_one_by_id(self, request: Request, id: UUID) -> Response:
        result: Result[Document] = await self.document_management.delete_one_by_id(
            state=request.state,
            id=id
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[Document](
                message=result.message,
                data=result.data
            ).json()
        )
        return response
