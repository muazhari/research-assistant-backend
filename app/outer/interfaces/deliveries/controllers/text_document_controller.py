from datetime import datetime, timedelta
from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.inner.model.entities.text_document import TextDocument
from app.inner.usecases.entity_manager.text_document_manager import text_document_manager

from app.outer.interfaces.deliveries.contracts.requests.entity_manager.text_document.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.text_document.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content

router = APIRouter(
    prefix="/documents/texts",
    tags=["/documents/texts"]
)


# read all text_document
@router.get(path="", response_model=Content[List[TextDocument]])
async def read_all() -> Content[List[TextDocument]]:
    return text_document_manager.read_all()


# read one text_document by id
@router.get(path="/{id}", response_model=Content[TextDocument])
async def read_one_by_id(id: UUID) -> Content[TextDocument]:
    return text_document_manager.read_one_by_id(id)


# create one text_document
@router.post(path="", response_model=Content[TextDocument])
async def create_one(entity_request: CreateOneRequest) -> Content[TextDocument]:
    return text_document_manager.create_one(entity_request)


# update one text_document by id
@router.patch(path="/{id}", response_model=Content[TextDocument])
async def patch_one_by_id(id: UUID, entity_request: PatchOneByIdRequest) -> Content[TextDocument]:
    return text_document_manager.patch_one_by_id(id, entity_request)


# delete one text_document by id
@router.delete(path="/{id}", response_model=Content[TextDocument])
async def delete_one_by_id(id: UUID) -> Content[TextDocument]:
    return text_document_manager.delete_one_by_id(id)


# delete one text_document by id
@router.delete(path="/{id}", response_model=Content[TextDocument])
async def delete_one_by_id(id: UUID) -> Content[TextDocument]:
    data: TextDocument = text_document_manager.delete_one_by_id(id)
    content: Content[TextDocument] = Content[TextDocument](
        message="Delete one text_document succeed.",
        data=data
    )
    return content
