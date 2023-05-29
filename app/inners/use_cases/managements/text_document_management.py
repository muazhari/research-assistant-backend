import uuid
from typing import List

from app.inners.models.entities.text_document import TextDocument
from app.inners.models.value_objects.contracts.requests.managements.text_documents.create_one_request import \
    CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.text_documents.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.text_documents.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.text_documents.read_all_request import \
    ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.text_documents.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.outers.repositories.text_document_repository import TextDocumentRepository
from app.outers.utilities.management_utility import ManagementUtility


class TextDocumentManagement:
    def __init__(self):
        self.management_utility: ManagementUtility = ManagementUtility()
        self.text_document_repository: TextDocumentRepository = TextDocumentRepository()

    async def read_all(self, request: ReadAllRequest) -> Content[List[TextDocument]]:
        try:
            found_entities: List[TextDocument] = await self.text_document_repository.read_all()

            if len(request.query_parameter.keys()) > 0:
                found_entities = list(
                    filter(
                        lambda entity: self.management_utility.filter(request.query_parameter, entity),
                        found_entities
                    )
                )

            content: Content[List[TextDocument]] = Content(
                data=found_entities,
                message="TextDocument read all succeed."
            )
        except Exception as exception:
            content: Content[List[TextDocument]] = Content(
                data=None,
                message=f"TextDocument read all failed: {exception}"
            )
        return content

    async def read_one_by_id(self, request: ReadOneByIdRequest) -> Content[TextDocument]:
        try:
            found_entity: TextDocument = await self.text_document_repository.read_one_by_id(request.id)
            content: Content[TextDocument] = Content(
                data=found_entity,
                message="TextDocument read one by id succeed."
            )
        except Exception as exception:
            content: Content[TextDocument] = Content(
                data=None,
                message=f"TextDocument read one by id failed: {exception}"
            )
        return content

    async def create_one(self, request: CreateOneRequest) -> Content[TextDocument]:
        try:
            entity_to_create: TextDocument = TextDocument(
                **request.body.dict(),
                id=uuid.uuid4(),
            )
            created_entity: TextDocument = await self.text_document_repository.create_one(entity_to_create)
            content: Content[TextDocument] = Content(
                data=created_entity,
                message="TextDocument create one succeed."
            )
        except Exception as exception:
            content: Content[TextDocument] = Content(
                data=None,
                message=f"TextDocument create one failed: {exception}"
            )
        return content

    async def patch_one_by_id(self, request: PatchOneByIdRequest) -> Content[TextDocument]:
        try:
            entity_to_patch: TextDocument = TextDocument(
                **request.body.dict(),
                id=request.id,
            )
            patched_entity: TextDocument = await self.text_document_repository.patch_one_by_id(request.id,
                                                                                               entity_to_patch)
            content: Content[TextDocument] = Content(
                data=patched_entity,
                message="TextDocument patch one by id succeed."
            )
        except Exception as exception:
            content: Content[TextDocument] = Content(
                data=None,
                message=f"TextDocument patch one by id failed: {exception}"
            )
        return content

    async def delete_one_by_id(self, request: DeleteOneByIdRequest) -> Content[TextDocument]:
        try:
            deleted_entity: TextDocument = await self.text_document_repository.delete_one_by_id(request.id)
            content: Content[TextDocument] = Content(
                data=deleted_entity,
                message="TextDocument delete one by id succeed."
            )
        except Exception as exception:
            content: Content[TextDocument] = Content(
                data=None,
                message=f"TextDocument delete one by id failed: {exception}"
            )
        return content
