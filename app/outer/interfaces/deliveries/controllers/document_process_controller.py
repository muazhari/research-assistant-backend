from datetime import datetime, timedelta
from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.inner.model.entities.document_process import DocumentProcess
from app.inner.usecases.entity_manager.document_process_manager import document_process_manager
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document_process.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document_process.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content

router = APIRouter(
    prefix="/documents/processes",
    tags=["/documents/processes"]
)


# read all document_process
@router.get(path="", response_model=Content[List[DocumentProcess]])
async def read_all() -> Content[List[DocumentProcess]]:
    return document_process_manager.read_all()


# read one document_process by id
@router.get(path="/{id}", response_model=Content[DocumentProcess])
async def read_one_by_id(id: UUID) -> Content[DocumentProcess]:
    return document_process_manager.read_one_by_id(id)


# create one document_process
@router.post(path="", response_model=Content[DocumentProcess])
async def create_one(entity_request: CreateOneRequest) -> Content[DocumentProcess]:
    return document_process_manager.create_one(entity_request)


# update one document_process by id
@router.patch(path="/{id}", response_model=Content[DocumentProcess])
async def patch_one_by_id(id: UUID, entity_request: PatchOneByIdRequest) -> Content[DocumentProcess]:
    return document_process_manager.patch_one_by_id(id, entity_request)


# delete one document_process by id
@router.delete(path="/{id}", response_model=Content[DocumentProcess])
async def delete_one_by_id(id: UUID) -> Content[DocumentProcess]:
    return document_process_manager.delete_one_by_id(id)
