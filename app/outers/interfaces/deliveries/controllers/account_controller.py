from typing import List
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request, Depends
from fastapi_utils.cbv import cbv

from app.inners.models.entities.account import Account
from app.inners.models.value_objects.contracts.requests.managements.accounts.create_body import \
    CreateBody
from app.inners.models.value_objects.contracts.requests.managements.accounts.create_one_request import \
    CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.accounts.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.accounts.patch_body import \
    PatchBody
from app.inners.models.value_objects.contracts.requests.managements.accounts.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.accounts.read_all_request import ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.accounts.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
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

    @router.get("/accounts")
    async def read_all(self, request: Request) -> Content[List[Account]]:
        request: ReadAllRequest = ReadAllRequest(query_parameter=dict(request.query_params))
        return await self.account_management.read_all(request=request)

    @router.get("/accounts/{id}")
    async def read_one_by_id(self, id: UUID) -> Content[Account]:
        request: ReadOneByIdRequest = ReadOneByIdRequest(id=id)
        return await self.account_management.read_one_by_id(request)

    @router.post("/accounts")
    async def create_one(self, body: CreateBody) -> Content[Account]:
        request: CreateOneRequest = CreateOneRequest(body=body)
        return await self.account_management.create_one(request)

    @router.patch("/accounts/{id}")
    async def patch_one_by_id(self, id: UUID, body: PatchBody) -> Content[Account]:
        request: PatchOneByIdRequest = PatchOneByIdRequest(id=id, body=body)
        return await self.account_management.patch_one_by_id(request)

    @router.delete("/accounts/{id}")
    async def delete_one_by_id(self, id: UUID) -> Content[Account]:
        request: DeleteOneByIdRequest = DeleteOneByIdRequest(id=id)
        return await self.account_management.delete_one_by_id(request)
