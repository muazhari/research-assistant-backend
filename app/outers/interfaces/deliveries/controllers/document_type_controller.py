from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette.requests import Request
from starlette.responses import Response

from app.inners.models.daos.document_type import DocumentType
from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.managements.document_types.patch_one_body import \
    PatchOneBody
from app.inners.models.dtos.contracts.result import Result
from app.inners.use_cases.managements.document_type_management import DocumentTypeManagement
from app.outers.containers.application_container import ApplicationContainer

router: APIRouter = APIRouter(tags=["document-types"])


@cbv(router)
class DocumentTypeController:

    @inject
    def __init__(
            self,
            document_type_management: DocumentTypeManagement = Depends(
                Provide[ApplicationContainer.use_cases.managements.document_type]
            )
    ) -> None:
        self.document_type_management: DocumentTypeManagement = document_type_management

    @router.get("/document-types/{id}")
    async def find_one_by_id(self, request: Request, id: str) -> Response:
        result: Result[DocumentType] = await self.document_type_management.find_one_by_id(
            state=request.state,
            id=id
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[DocumentType](
                message=result.message,
                data=result.data
            ).json()
        )
        return response

    @router.patch("/document-types/{id}")
    async def patch_one_by_id(self, request: Request, id: str, body: PatchOneBody) -> Response:
        result: Result[DocumentType] = await self.document_type_management.patch_one_by_id(
            state=request.state,
            id=id,
            body=body
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[DocumentType](
                message=result.message,
                data=result.data
            ).json()
        )
        return response
