from datetime import datetime, timedelta
from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.inner.model.entities.file_document import FileDocument
from app.inner.usecases.entity_manager.file_document_manager import file_document_manager
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.file_document.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.file_document.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content

router = APIRouter(
    prefix="/documents/files",
    tags=["/documents/files"]
)


# read all file_document
@router.get(path="", response_model=Content[List[FileDocument]])
async def read_all() -> Content[List[FileDocument]]:
    return file_document_manager.read_all()


# read one file_document by id
@router.get(path="/{id}", response_model=Content[FileDocument])
async def read_one_by_id(id: UUID) -> Content[FileDocument]:
    return file_document_manager.read_one_by_id(id)


# create one file_document
@router.post(path="", response_model=Content[FileDocument])
async def create_one(entity_request: CreateOneRequest) -> Content[FileDocument]:
    return file_document_manager.create_one(entity_request)


# update one file_document by id
@router.patch(path="/{id}", response_model=Content[FileDocument])
async def patch_one_by_id(id: UUID, entity_request: PatchOneByIdRequest) -> Content[FileDocument]:
    return file_document_manager.patch_one_by_id(id, entity_request)


# delete one file_document by id
@router.delete(path="/{id}", response_model=Content[FileDocument])
async def delete_one_by_id(id: UUID) -> Content[FileDocument]:
    return file_document_manager.delete_one_by_id(id)


# delete one file_document by id
@router.delete(path="/{id}", response_model=Content[FileDocument])
async def delete_one_by_id(id: UUID) -> Content[FileDocument]:
    data: FileDocument = file_document_manager.delete_one_by_id(id)
    content: Content[FileDocument] = Content[FileDocument](
        message="Delete one file_document succeed.",
        data=data
    )
    return content
