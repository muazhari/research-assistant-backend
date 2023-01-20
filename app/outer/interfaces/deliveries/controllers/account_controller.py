from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.inner.model.entities.account import Account
from app.inner.usecases.entity_manager.account_manager import account_manager
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.account.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.account.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content

router = APIRouter(
    prefix="/accounts",
    tags=["/accounts"]
)


# read all account
@router.get(path="", response_model=Content[List[Account]])
async def read_all() -> Content[List[Account]]:
    return account_manager.read_all()


# read one account by id
@router.get(path="/{id}", response_model=Content[Account])
async def read_one_by_id(id: UUID) -> Content[Account]:
    return account_manager.read_one_by_id(id)


# create one account
@router.post(path="", response_model=Content[Account])
async def create_one(entity_request: CreateOneRequest) -> Content[Account]:
    return account_manager.create_one(entity_request)


# update one account by id
@router.patch(path="/{id}", response_model=Content[Account])
async def patch_one_by_id(id: UUID, entity_request: PatchOneByIdRequest) -> Content[Account]:
    return account_manager.patch_one_by_id(id, entity_request)


# delete one account by id
@router.delete(path="/{id}", response_model=Content[Account])
async def delete_one_by_id(id: UUID) -> Content[Account]:
    return account_manager.delete_one_by_id(id)
