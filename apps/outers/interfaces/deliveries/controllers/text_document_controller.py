from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request, Depends
from fastapi_utils.cbv import cbv
from starlette.responses import Response

from apps.inners.models.dtos.contracts.content import Content
from apps.inners.models.dtos.contracts.requests.managements.text_documents.create_one_body import \
    CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.text_documents.patch_one_body import \
    PatchOneBody
from apps.inners.models.dtos.contracts.responses.managements.documents.text_document_response import \
    TextDocumentResponse
from apps.inners.models.dtos.contracts.result import Result
from apps.inners.use_cases.managements.text_document_management import TextDocumentManagement
from apps.outers.containers.application_container import ApplicationContainer

router: APIRouter = APIRouter(tags=["text-documents"])


@cbv(router)
class TextDocumentController:

    @inject
    def __init__(
            self,
            text_document_management: TextDocumentManagement = Depends(
                Provide[ApplicationContainer.use_cases.managements.text_document]
            )
    ) -> None:
        self.text_document_management = text_document_management

    @router.get("/documents/texts/{id}")
    async def find_one_by_id(self, request: Request, id: UUID) -> Response:
        result: Result[TextDocumentResponse] = await self.text_document_management.find_one_by_id(
            state=request.state,
            id=id
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[TextDocumentResponse](
                message=result.message,
                data=result.data
            ).json()
        )
        return response

    @router.post("/documents/texts")
    async def create_one(self, request: Request, body: CreateOneBody) -> Response:
        result: Result[TextDocumentResponse] = await self.text_document_management.create_one(
            state=request.state,
            body=body
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[TextDocumentResponse](
                message=result.message,
                data=result.data
            ).json()
        )
        return response

    @router.patch("/documents/texts/{id}")
    async def patch_one_by_id(self, request: Request, id: UUID, body: PatchOneBody) -> Response:
        result: Result[TextDocumentResponse] = await self.text_document_management.patch_one_by_id(
            state=request.state,
            id=id,
            body=body
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[TextDocumentResponse](
                message=result.message,
                data=result.data
            ).json()
        )
        return response

    @router.delete("/documents/texts/{id}")
    async def delete_one_by_id(self, request: Request, id: UUID) -> Response:
        result: Result[TextDocumentResponse] = await self.text_document_management.delete_one_by_id(
            state=request.state,
            id=id
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[TextDocumentResponse](
                message=result.message,
                data=result.data
            ).json()
        )
        return response
