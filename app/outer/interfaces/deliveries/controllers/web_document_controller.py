from datetime import datetime, timedelta
from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.inner.model.entities.web_document import WebDocument
from app.inner.usecases.entity_manager.web_document_manager import web_document_manager

from app.outer.interfaces.deliveries.contracts.requests.entity_manager.web_document.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.web_document.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content

router = APIRouter(
    prefix="/documents/webs",
    tags=["/documents/webs"]
)


# read all web_document
@router.get(path="", response_model=Content[List[WebDocument]])
async def read_all() -> Content[List[WebDocument]]:
    return web_document_manager.read_all()


# read one web_document by id
@router.get(path="/{id}", response_model=Content[WebDocument])
async def read_one_by_id(id: UUID) -> Content[WebDocument]:
    return web_document_manager.read_one_by_id(id)


# create one web_document
@router.post(path="", response_model=Content[WebDocument])
async def create_one(entity_request: CreateOneRequest) -> Content[WebDocument]:
    return web_document_manager.create_one(entity_request)


# update one web_document by id
@router.patch(path="/{id}", response_model=Content[WebDocument])
async def patch_one_by_id(id: UUID, entity_request: PatchOneByIdRequest) -> Content[WebDocument]:
    return web_document_manager.patch_one_by_id(id, entity_request)


# delete one web_document by id
@router.delete(path="/{id}", response_model=Content[WebDocument])
async def delete_one_by_id(id: UUID) -> Content[WebDocument]:
    return web_document_manager.delete_one_by_id(id)


# delete one web_document by id
@router.delete(path="/{id}", response_model=Content[WebDocument])
async def delete_one_by_id(id: UUID) -> Content[WebDocument]:
    data: WebDocument = web_document_manager.delete_one_by_id(id)
    content: Content[WebDocument] = Content[WebDocument](
        message="Delete one web_document succeed.",
        data=data
    )
    return content
