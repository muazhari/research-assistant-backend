import uuid
from datetime import datetime, timezone
from typing import List

from app.inners.models.entities.web_document import WebDocument
from app.inners.models.value_objects.contracts.requests.managements.web_documents.create_one_request import \
    CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.web_documents.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.web_documents.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.web_documents.read_all_request import ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.web_documents.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.outers.repositories.web_document_repository import WebDocumentRepository
from app.outers.utilities.management_utility import ManagementUtility


class WebDocumentManagement:
    def __init__(self):
        self.management_utility: ManagementUtility = ManagementUtility()
        self.web_document_repository: WebDocumentRepository = WebDocumentRepository()

    async def read_all(self, request: ReadAllRequest) -> Content[List[WebDocument]]:
        try:
            found_entities: List[WebDocument] = await self.web_document_repository.read_all()

            if len(request.query_parameter.keys()) > 0:
                found_entities = list(
                    filter(
                        lambda entity: self.management_utility.filter(request.query_parameter, entity),
                        found_entities
                    )
                )

            content: Content[List[WebDocument]] = Content(
                data=found_entities,
                message="WebDocument read all succeed."
            )
        except Exception as exception:
            content: Content[List[WebDocument]] = Content(
                data=None,
                message=f"WebDocument read all failed: {exception}"
            )
        return content

    async def read_one_by_id(self, request: ReadOneByIdRequest) -> Content[WebDocument]:
        try:
            found_entity: WebDocument = await self.web_document_repository.read_one_by_id(request.id)
            content: Content[WebDocument] = Content(
                data=found_entity,
                message="WebDocument read one by id succeed."
            )
        except Exception as exception:
            content: Content[WebDocument] = Content(
                data=None,
                message=f"WebDocument read one by id failed: {exception}"
            )
        return content

    async def create_one(self, request: CreateOneRequest) -> Content[WebDocument]:
        try:
            timestamp: datetime = datetime.now(tz=timezone.utc)
            entity_to_create: WebDocument = WebDocument(
                **request.body.dict(),
                id=uuid.uuid4(),
                created_at=timestamp,
                updated_at=timestamp,
            )
            created_entity: WebDocument = await self.web_document_repository.create_one(entity_to_create)
            content: Content[WebDocument] = Content(
                data=created_entity,
                message="WebDocument create one succeed."
            )
        except Exception as exception:
            content: Content[WebDocument] = Content(
                data=None,
                message=f"WebDocument create one failed: {exception}"
            )
        return content

    async def patch_one_by_id(self, request: PatchOneByIdRequest) -> Content[WebDocument]:
        try:
            entity_to_patch: WebDocument = WebDocument(
                **request.body.dict(),
                id=request.id,
                updated_at=datetime.now(tz=timezone.utc),
            )
            patched_entity: WebDocument = await self.web_document_repository.patch_one_by_id(request.id,
                                                                                             entity_to_patch)
            content: Content[WebDocument] = Content(
                data=patched_entity,
                message="WebDocument patch one by id succeed."
            )
        except Exception as exception:
            content: Content[WebDocument] = Content(
                data=None,
                message=f"WebDocument patch one by id failed: {exception}"
            )
        return content

    async def delete_one_by_id(self, request: DeleteOneByIdRequest) -> Content[WebDocument]:
        try:
            deleted_entity: WebDocument = await self.web_document_repository.delete_one_by_id(request.id)
            content: Content[WebDocument] = Content(
                data=deleted_entity,
                message="WebDocument delete one by id succeed."
            )
        except Exception as exception:
            content: Content[WebDocument] = Content(
                data=None,
                message=f"WebDocument delete one by id failed: {exception}"
            )
        return content
