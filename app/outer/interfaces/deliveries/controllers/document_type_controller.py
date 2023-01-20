from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.inner.model.entities.document_type import DocumentType
from app.inner.usecases.entity_manager.document_type_manager import document_type_manager
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document_type.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document_type.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content

router = APIRouter(
    prefix="/documents/types",
    tags=["/documents/types"]
)


# read all document_type
@router.get(path="", response_model=Content[List[DocumentType]])
async def read_all() -> Content[List[DocumentType]]:
    return document_type_manager.read_all()


# read one document_type by id
@router.get(path="/{id}", response_model=Content[DocumentType])
async def read_one_by_id(id: UUID) -> Content[DocumentType]:
    return document_type_manager.read_one_by_id(id)


# create one document_type
@router.post(path="", response_model=Content[DocumentType])
async def create_one(entity_request: CreateOneRequest) -> Content[DocumentType]:
    return document_type_manager.create_one(entity_request)


# update one document_type by id
@router.patch(path="/{id}", response_model=Content[DocumentType])
async def patch_one_by_id(id: UUID, entity_request: PatchOneByIdRequest) -> Content[DocumentType]:
    return document_type_manager.patch_one_by_id(id, entity_request)


# delete one document_type by id
@router.delete(path="/{id}", response_model=Content[DocumentType])
async def delete_one_by_id(id: UUID) -> Content[DocumentType]:
    return document_type_manager.delete_one_by_id(id)


# delete one document_type by id
@router.delete(path="/{id}", response_model=Content[DocumentType])
async def delete_one_by_id(id: UUID) -> Content[DocumentType]:
    data: DocumentType = document_type_manager.delete_one_by_id(id)
    content: Content[DocumentType] = Content[DocumentType](
        message="Delete one document_type succeed.",
        data=data
    )
    return content
