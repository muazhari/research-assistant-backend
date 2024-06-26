from starlette.datastructures import State

from apps.inners.models.daos.document_type import DocumentType
from apps.inners.models.dtos.contracts.requests.managements.document_types.patch_one_body import PatchOneBody
from apps.outers.repositories.document_type_repository import DocumentTypeRepository


class DocumentTypeManagement:
    def __init__(
            self,
            document_type_repository: DocumentTypeRepository,
    ):
        self.document_type_repository: DocumentTypeRepository = document_type_repository

    async def find_one_by_id(self, state: State, id: str) -> DocumentType:
        found_document_type: DocumentType = await self.document_type_repository.find_one_by_id(
            session=state.session,
            id=id
        )
        return found_document_type

    async def patch_one_by_id(self, state: State, id: str, body: PatchOneBody) -> DocumentType:
        document_type_patcher: DocumentType = DocumentType(**body.dict())
        patched_document_type: DocumentType = await self.patch_one_by_id_raw(
            state=state,
            id=id,
            document_type_patcher=document_type_patcher
        )
        return patched_document_type

    async def patch_one_by_id_raw(self, state: State, id: str, document_type_patcher: DocumentType) -> \
            DocumentType:
        patched_document_type: DocumentType = await self.document_type_repository.patch_one_by_id(
            session=state.session,
            id=id,
            document_type_patcher=document_type_patcher
        )
        return patched_document_type
