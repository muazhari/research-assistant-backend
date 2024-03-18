from sqlalchemy import exc
from starlette import status
from starlette.datastructures import State

from app.inners.models.daos.document_type import DocumentType
from app.inners.models.dtos.contracts.requests.managements.document_types.create_one_body import CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.document_types.patch_one_body import PatchOneBody
from app.inners.models.dtos.contracts.result import Result
from app.outers.repositories.document_type_repository import DocumentTypeRepository


class DocumentTypeManagement:
    def __init__(
            self,
            document_type_repository: DocumentTypeRepository,
    ):
        self.document_type_repository: DocumentTypeRepository = document_type_repository

    async def find_one_by_id(self, state: State, id: str) -> Result[DocumentType]:
        try:
            found_document_type: DocumentType = await self.document_type_repository.find_one_by_id(
                session=state.session,
                id=id
            )
            result: Result[DocumentType] = Result(
                status_code=status.HTTP_200_OK,
                message="DocumentTypeManagement.find_one_by_id: Succeed.",
                data=found_document_type,
            )
        except exc.NoResultFound:
            result: Result[DocumentType] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="DocumentTypeManagement.find_one_by_id: Failed, document_type is not found.",
                data=None,
            )
        return result

    async def create_one(self, state: State, body: CreateOneBody) -> Result[DocumentType]:
        document_type_creator: DocumentType = DocumentType(**body.dict())
        created_document_type: DocumentType = await self.document_type_repository.create_one(
            session=state.session,
            document_type_creator=document_type_creator
        )
        result: Result[DocumentType] = Result(
            status_code=status.HTTP_201_CREATED,
            message="DocumentTypeManagement.create_one: Succeed.",
            data=created_document_type,
        )
        return result

    async def create_one_raw(self, state: State, document_type_creator: DocumentType) -> Result[
        DocumentType]:
        created_document_type: DocumentType = await self.document_type_repository.create_one(
            session=state.session,
            document_type_creator=document_type_creator
        )
        result: Result[DocumentType] = Result(
            status_code=status.HTTP_201_CREATED,
            message="DocumentTypeManagement.create_one_raw: Succeed.",
            data=created_document_type,
        )
        return result

    async def patch_one_by_id(self, state: State, id: str, body: PatchOneBody) -> Result[DocumentType]:
        try:
            document_type_patcher: DocumentType = DocumentType(**body.dict())
            patched_document_type: DocumentType = await self.document_type_repository.patch_one_by_id(
                session=state.session,
                id=id,
                document_type_patcher=document_type_patcher
            )
            result: Result[DocumentType] = Result(
                status_code=status.HTTP_200_OK,
                message="DocumentTypeManagement.patch_one_by_id: Succeed.",
                data=patched_document_type,
            )
        except exc.NoResultFound:
            result: Result[DocumentType] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="DocumentTypeManagement.patch_one_by_id: Failed, document_type is not found.",
                data=None,
            )
        return result

    async def patch_one_by_id_raw(self, state: State, id: str, document_type_patcher: DocumentType) -> \
            Result[DocumentType]:
        patched_document_type: DocumentType = await self.document_type_repository.patch_one_by_id(
            session=state.session,
            id=id,
            document_type_patcher=document_type_patcher
        )
        result: Result[DocumentType] = Result(
            status_code=status.HTTP_200_OK,
            message="DocumentTypeManagement.patch_one_by_id_raw: Succeed.",
            data=patched_document_type,
        )
        return result

    async def delete_one_by_id(self, state: State, id: str) -> Result[DocumentType]:
        try:
            deleted_document_type: DocumentType = await self.document_type_repository.delete_one_by_id(
                session=state.session,
                id=id
            )
            result: Result[DocumentType] = Result(
                status_code=status.HTTP_200_OK,
                message="DocumentTypeManagement.delete_one_by_id: Succeed.",
                data=deleted_document_type,
            )
        except exc.NoResultFound:
            result: Result[DocumentType] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="DocumentTypeManagement.delete_one_by_id: Failed, document_type is not found.",
                data=None,
            )
        return result
