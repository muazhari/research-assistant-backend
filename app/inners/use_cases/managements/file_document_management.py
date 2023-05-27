import uuid
from datetime import datetime, timezone
from typing import List

from app.inners.models.entities.file_document import FileDocument
from app.inners.models.value_objects.contracts.requests.managements.file_documents.create_one_request import \
    CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.file_documents.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.file_documents.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.file_documents.read_all_request import \
    ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.file_documents.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.outers.repositories.file_document_repository import FileDocumentRepository
from app.outers.utilities.management_utility import ManagementUtility


class FileDocumentManagement:
    def __init__(self):
        self.management_utility: ManagementUtility = ManagementUtility()
        self.file_document_repository: FileDocumentRepository = FileDocumentRepository()

    async def read_all(self, request: ReadAllRequest) -> Content[List[FileDocument]]:
        try:
            found_entities: List[FileDocument] = await self.file_document_repository.read_all()

            if len(request.query_parameter.keys()) > 0:
                found_entities = list(
                    filter(
                        lambda entity: self.management_utility.filter(request.query_parameter, entity),
                        found_entities
                    )
                )

            content: Content[List[FileDocument]] = Content(
                data=found_entities,
                message="FileDocument read all succeed."
            )
        except Exception as exception:
            content: Content[List[FileDocument]] = Content(
                data=None,
                message=f"FileDocument read all failed: {exception}"
            )
        return content

    async def read_one_by_id(self, request: ReadOneByIdRequest) -> Content[FileDocument]:
        try:
            found_entity: FileDocument = await self.file_document_repository.read_one_by_id(request.id)
            content: Content[FileDocument] = Content(
                data=found_entity,
                message="FileDocument read one by id succeed."
            )
        except Exception as exception:
            content: Content[FileDocument] = Content(
                data=None,
                message=f"FileDocument read one by id failed: {exception}"
            )
        return content

    async def create_one(self, request: CreateOneRequest) -> Content[FileDocument]:
        try:
            timestamp: datetime = datetime.now(tz=timezone.utc)
            entity_to_create: FileDocument = FileDocument(
                **request.body.dict(),
                id=uuid.uuid4(),
                created_at=timestamp,
                updated_at=timestamp,
            )
            created_entity: FileDocument = await self.file_document_repository.create_one(entity_to_create)
            content: Content[FileDocument] = Content(
                data=created_entity,
                message="FileDocument create one succeed."
            )
        except Exception as exception:
            content: Content[FileDocument] = Content(
                data=None,
                message=f"FileDocument create one failed: {exception}"
            )
        return content

    async def patch_one_by_id(self, request: PatchOneByIdRequest) -> Content[FileDocument]:
        try:
            entity_to_patch: FileDocument = FileDocument(
                **request.body.dict(),
                id=request.id,
                updated_at=datetime.now(tz=timezone.utc),
            )
            patched_entity: FileDocument = await self.file_document_repository.patch_one_by_id(request.id,
                                                                                               entity_to_patch)
            content: Content[FileDocument] = Content(
                data=patched_entity,
                message="FileDocument patch one by id succeed."
            )
        except Exception as exception:
            content: Content[FileDocument] = Content(
                data=None,
                message=f"FileDocument patch one by id failed: {exception}"
            )
        return content

    async def delete_one_by_id(self, request: DeleteOneByIdRequest) -> Content[FileDocument]:
        try:
            deleted_entity: FileDocument = await self.file_document_repository.delete_one_by_id(request.id)
            content: Content[FileDocument] = Content(
                data=deleted_entity,
                message="FileDocument delete one by id succeed."
            )
        except Exception as exception:
            content: Content[FileDocument] = Content(
                data=None,
                message=f"FileDocument delete one by id failed: {exception}"
            )
        return content
