import uuid
from typing import List

from app.inners.models.entities.document_type import DocumentType
from app.inners.models.value_objects.contracts.requests.managements.document_types.create_one_request import \
    CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.document_types.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.document_types.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.document_types.read_all_request import \
    ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.document_types.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.use_cases.utilities.management_utility import ManagementUtility
from app.outers.repositories.document_type_repository import DocumentTypeRepository


class DocumentTypeManagement:
    def __init__(
            self,
            document_type_repository: DocumentTypeRepository,
            management_utility: ManagementUtility
    ):
        self.document_type_repository: DocumentTypeRepository = document_type_repository
        self.management_utility: ManagementUtility = management_utility

    async def read_all(self, request: ReadAllRequest) -> Content[List[DocumentType]]:
        try:
            found_entities: List[DocumentType] = await self.document_type_repository.read_all()

            if len(request.query_parameter.keys()) > 0:
                found_entities = list(
                    filter(
                        lambda entity: self.management_utility.filter(request.query_parameter, entity),
                        found_entities
                    )
                )

            content: Content[List[DocumentType]] = Content(
                data=found_entities,
                message="DocumentType read all succeed."
            )
        except Exception as exception:
            content: Content[List[DocumentType]] = Content(
                data=None,
                message=f"DocumentType read all failed: {exception}"
            )
        return content

    async def read_one_by_id(self, request: ReadOneByIdRequest) -> Content[DocumentType]:
        try:
            found_entity: DocumentType = await self.document_type_repository.read_one_by_id(request.id)
            content: Content[DocumentType] = Content(
                data=found_entity,
                message="DocumentType read one by id succeed."
            )
        except Exception as exception:
            content: Content[DocumentType] = Content(
                data=None,
                message=f"DocumentType read one by id failed: {exception}"
            )
        return content

    async def create_one(self, request: CreateOneRequest) -> Content[DocumentType]:
        try:
            entity_to_create: DocumentType = DocumentType(
                **request.body.dict(),
                id=uuid.uuid4(),
            )
            created_entity: DocumentType = await self.document_type_repository.create_one(entity_to_create)
            content: Content[DocumentType] = Content(
                data=created_entity,
                message="DocumentType create one succeed."
            )
        except Exception as exception:
            content: Content[DocumentType] = Content(
                data=None,
                message=f"DocumentType create one failed: {exception}"
            )
        return content

    async def patch_one_by_id(self, request: PatchOneByIdRequest) -> Content[DocumentType]:
        try:
            entity_to_patch: DocumentType = DocumentType(
                **request.body.dict(),
                id=request.id,
            )
            patched_entity: DocumentType = await self.document_type_repository.patch_one_by_id(request.id,
                                                                                               entity_to_patch)
            content: Content[DocumentType] = Content(
                data=patched_entity,
                message="DocumentType patch one by id succeed."
            )
        except Exception as exception:
            content: Content[DocumentType] = Content(
                data=None,
                message=f"DocumentType patch one by id failed: {exception}"
            )
        return content

    async def delete_one_by_id(self, request: DeleteOneByIdRequest) -> Content[DocumentType]:
        try:
            deleted_entity: DocumentType = await self.document_type_repository.delete_one_by_id(request.id)
            content: Content[DocumentType] = Content(
                data=deleted_entity,
                message="DocumentType delete one by id succeed."
            )
        except Exception as exception:
            content: Content[DocumentType] = Content(
                data=None,
                message=f"DocumentType delete one by id failed: {exception}"
            )
        return content
