from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request, Depends
from fastapi_utils.cbv import cbv
from starlette.responses import Response

from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.managements.file_documents.create_one_body import \
    CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.file_documents.patch_one_body import \
    PatchOneBody
from app.inners.models.dtos.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from app.inners.models.dtos.contracts.result import Result
from app.inners.use_cases.managements.file_document_management import FileDocumentManagement
from app.outers.containers.application_container import ApplicationContainer

router: APIRouter = APIRouter(tags=["file-documents"])


@cbv(router)
class FileDocumentController:

    @inject
    def __init__(
            self,
            file_document_management: FileDocumentManagement = Depends(
                Provide[ApplicationContainer.use_cases.managements.file_document]
            )
    ) -> None:
        self.file_document_management = file_document_management

    @router.get("/documents/files/{id}")
    async def find_one_by_id(self, request: Request, id: UUID) -> Response:
        result: Result[FileDocumentResponse] = await self.file_document_management.find_one_by_id(
            session=request.state.session,
            id=id
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[FileDocumentResponse](
                message=result.message,
                data=result.data
            )
        )
        return response

    @router.post("/documents/files")
    async def create_one(self, request: Request, body: CreateOneBody) -> Response:
        result: Result[FileDocumentResponse] = await self.file_document_management.create_one(
            session=request.state.session,
            body=body
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[FileDocumentResponse](
                message=result.message,
                data=result.data
            )
        )
        return response

    @router.patch("/documents/files/{id}")
    async def patch_one_by_id(self, request: Request, id: UUID, body: PatchOneBody) -> Response:
        result: Result[FileDocumentResponse] = await self.file_document_management.patch_one_by_id(
            session=request.state.session,
            id=id,
            body=body
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[FileDocumentResponse](
                message=result.message,
                data=result.data
            )
        )
        return response

    @router.delete("/documents/files/{id}")
    async def delete_one_by_id(self, request: Request, id: UUID) -> Response:
        result: Result[FileDocumentResponse] = await self.file_document_management.delete_one_by_id(
            session=request.state.session,
            id=id
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[FileDocumentResponse](
                message=result.message,
                data=result.data
            )
        )
        return response
