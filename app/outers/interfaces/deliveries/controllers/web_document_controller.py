from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request, Depends
from fastapi_utils.cbv import cbv
from starlette.responses import Response

from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.managements.web_documents.create_one_body import \
    CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.web_documents.patch_one_body import \
    PatchOneBody
from app.inners.models.dtos.contracts.responses.managements.documents.web_document_response import \
    WebDocumentResponse
from app.inners.models.dtos.contracts.result import Result
from app.inners.use_cases.managements.web_document_management import WebDocumentManagement
from app.outers.containers.application_container import ApplicationContainer

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
        result: Result[WebDocumentResponse] = await self.web_document_management.find_one_by_id(
            state=request.state,
            id=id
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[WebDocumentResponse](
                message=result.message,
                data=result.data
            ).json()
        )
        return response

    @router.post("/documents/webs")
    async def create_one(self, request: Request, body: CreateOneBody) -> Response:
        result: Result[WebDocumentResponse] = await self.web_document_management.create_one(
            state=request.state,
            body=body
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[WebDocumentResponse](
                message=result.message,
                data=result.data
            ).json()
        )
        return response

    @router.patch("/documents/webs/{id}")
    async def patch_one_by_id(self, request: Request, id: UUID, body: PatchOneBody) -> Response:
        result: Result[WebDocumentResponse] = await self.web_document_management.patch_one_by_id(
            state=request.state,
            id=id,
            body=body
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[WebDocumentResponse](
                message=result.message,
                data=result.data
            ).json()
        )
        return response

    @router.delete("/documents/webs/{id}")
    async def delete_one_by_id(self, request: Request, id: UUID) -> Response:
        result: Result[WebDocumentResponse] = await self.web_document_management.delete_one_by_id(
            state=request.state,
            id=id
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[WebDocumentResponse](
                message=result.message,
                data=result.data
            ).json()
        )
        return response
