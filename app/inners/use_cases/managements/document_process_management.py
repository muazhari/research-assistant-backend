import uuid
from typing import List

from app.inners.models.entities.document_process import DocumentProcess
from app.inners.models.value_objects.contracts.requests.managements.document_processes.create_one_request import \
    CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.document_processes.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.document_processes.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.document_processes.read_all_request import \
    ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.document_processes.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.outers.repositories.document_process_repository import DocumentProcessRepository
from app.outers.utilities.management_utility import ManagementUtility


class DocumentProcessManagement:
    def __init__(self):
        self.management_utility: ManagementUtility = ManagementUtility()
        self.document_process_repository: DocumentProcessRepository = DocumentProcessRepository()

    async def read_all(self, request: ReadAllRequest) -> Content[List[DocumentProcess]]:
        try:
            found_entities: List[DocumentProcess] = await self.document_process_repository.read_all()

            if len(request.query_parameter.keys()) > 0:
                found_entities = list(
                    filter(
                        lambda entity: self.management_utility.filter(request.query_parameter, entity),
                        found_entities
                    )
                )

            content: Content[List[DocumentProcess]] = Content(
                data=found_entities,
                message="DocumentProcess read all succeed."
            )
        except Exception as exception:
            content: Content[List[DocumentProcess]] = Content(
                data=None,
                message=f"DocumentProcess read all failed: {exception}"
            )
        return content

    async def read_one_by_id(self, request: ReadOneByIdRequest) -> Content[DocumentProcess]:
        try:
            found_entity: DocumentProcess = await self.document_process_repository.read_one_by_id(request.id)
            content: Content[DocumentProcess] = Content(
                data=found_entity,
                message="DocumentProcess read one by id succeed."
            )
        except Exception as exception:
            content: Content[DocumentProcess] = Content(
                data=None,
                message=f"DocumentProcess read one by id failed: {exception}"
            )
        return content

    async def create_one(self, request: CreateOneRequest) -> Content[DocumentProcess]:
        try:
            entity_to_create: DocumentProcess = DocumentProcess(
                **request.body.dict(),
                id=uuid.uuid4(),
            )
            created_entity: DocumentProcess = await self.document_process_repository.create_one(entity_to_create)
            content: Content[DocumentProcess] = Content(
                data=created_entity,
                message="DocumentProcess create one succeed."
            )
        except Exception as exception:
            content: Content[DocumentProcess] = Content(
                data=None,
                message=f"DocumentProcess create one failed: {exception}"
            )
        return content

    async def patch_one_by_id(self, request: PatchOneByIdRequest) -> Content[DocumentProcess]:
        try:
            entity_to_patch: DocumentProcess = DocumentProcess(
                **request.body.dict(),
                id=request.id,
            )
            patched_entity: DocumentProcess = await self.document_process_repository.patch_one_by_id(request.id,
                                                                                                     entity_to_patch)
            content: Content[DocumentProcess] = Content(
                data=patched_entity,
                message="DocumentProcess patch one by id succeed."
            )
        except Exception as exception:
            content: Content[DocumentProcess] = Content(
                data=None,
                message=f"DocumentProcess patch one by id failed: {exception}"
            )
        return content

    async def delete_one_by_id(self, request: DeleteOneByIdRequest) -> Content[DocumentProcess]:
        try:
            deleted_entity: DocumentProcess = await self.document_process_repository.delete_one_by_id(request.id)
            content: Content[DocumentProcess] = Content(
                data=deleted_entity,
                message="DocumentProcess delete one by id succeed."
            )
        except Exception as exception:
            content: Content[DocumentProcess] = Content(
                data=None,
                message=f"DocumentProcess delete one by id failed: {exception}"
            )
        return content
