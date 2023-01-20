from datetime import datetime, timedelta
from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.inner.model.entities.document import Document
from app.inner.usecases.entity_manager.document_manager import document_manager
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content

router = APIRouter(
    prefix="/documents",
    tags=["/documents"]
)


# read all document
@router.get(path="", response_model=Content[List[Document]])
async def read_all() -> Content[List[Document]]:
    return document_manager.read_all()


# read one document by id
@router.get(path="/{id}", response_model=Content[Document])
async def read_one_by_id(id: UUID) -> Content[Document]:
    return document_manager.read_one_by_id(id)


# create one document
@router.post(path="", response_model=Content[Document])
async def create_one(entity_request: CreateOneRequest) -> Content[Document]:
    return document_manager.create_one(entity_request)


# update one document by id
@router.patch(path="/{id}", response_model=Content[Document])
async def patch_one_by_id(id: UUID, entity_request: PatchOneByIdRequest) -> Content[Document]:
    return document_manager.patch_one_by_id(id, entity_request)


# delete one document by id
@router.delete(path="/{id}", response_model=Content[Document])
async def delete_one_by_id(id: UUID) -> Content[Document]:
    return document_manager.delete_one_by_id(id)

