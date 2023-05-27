import uuid
from datetime import datetime, timezone
from typing import List

from app.inners.models.entities.document import Document
from app.inners.models.value_objects.contracts.requests.managements.documents.create_one_request import CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.documents.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.documents.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.documents.read_all_request import ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.documents.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.outers.repositories.document_repository import DocumentRepository
from app.outers.utilities.management_utility import ManagementUtility


class DocumentManagement:
    def __init__(self):
        self.management_utility: ManagementUtility = ManagementUtility()
        self.document_repository: DocumentRepository = DocumentRepository()

    async def read_all(self, request: ReadAllRequest) -> Content[List[Document]]:
        try:
            found_entities: List[Document] = await self.document_repository.read_all()

            if len(request.query_parameter.keys()) > 0:
                found_entities = list(
                    filter(
                        lambda entity: self.management_utility.filter(request.query_parameter, entity),
                        found_entities
                    )
                )

            content: Content[List[Document]] = Content(
                data=found_entities,
                message="Document read all succeed."
            )
        except Exception as exception:
            content: Content[List[Document]] = Content(
                data=None,
                message=f"Document read all failed: {exception}"
            )
        return content

    async def read_one_by_id(self, request: ReadOneByIdRequest) -> Content[Document]:
        try:
            found_entity: Document = await self.document_repository.read_one_by_id(request.id)
            content: Content[Document] = Content(
                data=found_entity,
                message="Document read one by id succeed."
            )
        except Exception as exception:
            content: Content[Document] = Content(
                data=None,
                message=f"Document read one by id failed: {exception}"
            )
        return content

    async def create_one(self, request: CreateOneRequest) -> Content[Document]:
        try:
            timestamp: datetime = datetime.now(tz=timezone.utc)
            entity_to_create: Document = Document(
                **request.body.dict(),
                id=uuid.uuid4(),
                created_at=timestamp,
                updated_at=timestamp,
            )
            created_entity: Document = await self.document_repository.create_one(entity_to_create)
            content: Content[Document] = Content(
                data=created_entity,
                message="Document create one succeed."
            )
        except Exception as exception:
            content: Content[Document] = Content(
                data=None,
                message=f"Document create one failed: {exception}"
            )
        return content

    async def patch_one_by_id(self, request: PatchOneByIdRequest) -> Content[Document]:
        try:
            entity_to_patch: Document = Document(
                **request.body.dict(),
                id=request.id,
                updated_at=datetime.now(tz=timezone.utc),
            )
            patched_entity: Document = await self.document_repository.patch_one_by_id(request.id, entity_to_patch)
            content: Content[Document] = Content(
                data=patched_entity,
                message="Document patch one by id succeed."
            )
        except Exception as exception:
            content: Content[Document] = Content(
                data=None,
                message=f"Document patch one by id failed: {exception}"
            )
        return content

    async def delete_one_by_id(self, request: DeleteOneByIdRequest) -> Content[Document]:
        try:
            deleted_entity: Document = await self.document_repository.delete_one_by_id(request.id)
            content: Content[Document] = Content(
                data=deleted_entity,
                message="Document delete one by id succeed."
            )
        except Exception as exception:
            content: Content[Document] = Content(
                data=None,
                message=f"Document delete one by id failed: {exception}"
            )
        return content
