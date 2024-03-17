from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette.requests import Request
from starlette.responses import Response

from app.inners.models.daos.account import Account
from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.managements.accounts.create_one_body import \
    CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.accounts.patch_one_body import \
    PatchOneBody
from app.inners.models.dtos.contracts.result import Result
from app.inners.use_cases.managements.account_management import AccountManagement
from app.outers.containers.application_container import ApplicationContainer

router: APIRouter = APIRouter(tags=["accounts"])


@cbv(router)
class AccountController:

    @inject
    def __init__(
            self,
            account_management: AccountManagement = Depends(
                Provide[ApplicationContainer.use_cases.managements.account]
            )
    ) -> None:
        self.account_management: AccountManagement = account_management

    @router.get("/accounts/{id}")
    async def find_one_by_id(self, request: Request, id: UUID) -> Response:
        result: Result[Account] = await self.account_management.find_one_by_id(
            state=request.state,
            id=id
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[Account](
                message=result.message,
                data=result.data
            )
        )
        return response

    @router.post("/accounts")
    async def create_one(self, request: Request, body: CreateOneBody) -> Response:
        result: Result[Account] = await self.account_management.create_one(
            state=request.state,
            body=body
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[Account](
                message=result.message,
                data=result.data
            )
        )
        return response

    @router.patch("/accounts/{id}")
    async def patch_one_by_id(self, request: Request, id: UUID, body: PatchOneBody) -> Response:
        result: Result[Account] = await self.account_management.patch_one_by_id(
            state=request.state,
            id=id,
            body=body
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[Account](
                message=result.message,
                data=result.data
            )
        )
        return response

    @router.delete("/accounts/{id}")
    async def delete_one_by_id(self, request: Request, id: UUID) -> Response:
        result: Result[Account] = await self.account_management.delete_one_by_id(
            state=request.state,
            id=id
        )
        response: Response = Response(
            status_code=result.status_code,
            content=Content[Account](
                message=result.message,
                data=result.data
            )
        )
        return response
