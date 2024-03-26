import hashlib
import uuid
from uuid import UUID

from sqlalchemy import exc
from starlette import status
from starlette.datastructures import State

from app.inners.models.daos.document import Document
from app.inners.models.daos.file_document import FileDocument
from app.inners.models.dtos.contracts.requests.managements.file_documents.create_one_body import CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.file_documents.patch_one_body import PatchOneBody
from app.inners.models.dtos.contracts.responses.managements.documents.file_document_response import FileDocumentResponse
from app.inners.models.dtos.contracts.result import Result
from app.inners.use_cases.managements.document_management import DocumentManagement
from app.outers.interfaces.deliveries.middlewares.session_middleware import SessionMiddleware
from app.outers.repositories.file_document_repository import FileDocumentRepository


class FileDocumentManagement:
    def __init__(
            self,
            document_management: DocumentManagement,
            file_document_repository: FileDocumentRepository,
    ):
        self.document_management: DocumentManagement = document_management
        self.file_document_repository: FileDocumentRepository = file_document_repository

    async def find_one_by_id(self, state: State, id: UUID) -> Result[FileDocumentResponse]:
        try:
            found_document: Result[Document] = await self.document_management.find_one_by_id(
                state=state,
                id=id
            )
            if found_document.status_code != status.HTTP_200_OK:
                return Result(
                    status_code=found_document.status_code,
                    message=f"FileDocumentManagement.find_one_by_id: Failed, {found_document.message}",
                    data=None,
                )
            found_file_document: FileDocument = await self.file_document_repository.find_one_by_id(
                session=state.session,
                id=id
            )
            found_file_document_response: FileDocumentResponse = FileDocumentResponse(
                id=found_document.data.id,
                document_name=found_document.data.name,
                document_description=found_document.data.description,
                document_type_id=found_document.data.document_type_id,
                document_account_id=found_document.data.account_id,
                file_name=found_file_document.file_name,
                file_data_hash=found_file_document.file_data_hash,
                file_meta=dict()
            )
            result: Result[FileDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="FileDocumentManagement.find_one_by_id: Succeed.",
                data=found_file_document_response,
            )
        except exc.NoResultFound:
            result: Result[FileDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="FileDocumentManagement.find_one_by_id: Failed, file_document is not found.",
                data=None,
            )
        return result

    async def create_one(self, state: State, body: CreateOneBody) -> Result[FileDocumentResponse]:
        document_creator: Document = Document(
            id=uuid.uuid4(),
            name=body.document_name,
            description=body.document_description,
            document_type_id=body.document_type_id,
            account_id=body.document_account_id
        )
        created_document: Result[Document] = await self.document_management.create_one_raw(
            state=state,
            document_creator=document_creator
        )
        if created_document.status_code != status.HTTP_201_CREATED:
            result: Result[FileDocumentResponse] = Result(
                status_code=created_document.status_code,
                message=f"FileDocumentManagement.create_one: Failed, {created_document.message}",
                data=None,
            )
            raise SessionMiddleware.HandlerException(
                result=result
            )

        file_data: bytes = await body.file_data.read()
        await body.file_data.close()
        file_document_creator: FileDocument = FileDocument(
            id=created_document.data.id,
            file_name=body.file_name,
            file_data_hash=hashlib.sha256(file_data).hexdigest()
        )
        created_file_document: FileDocument = await self.file_document_repository.create_one(
            session=state.session,
            file_document_creator=file_document_creator,
            file_data=file_data
        )
        file_document_response: FileDocumentResponse = FileDocumentResponse(
            id=created_document.data.id,
            document_name=created_document.data.name,
            document_description=created_document.data.description,
            document_type_id=created_document.data.document_type_id,
            document_account_id=created_document.data.account_id,
            file_name=created_file_document.file_name,
            file_data_hash=created_file_document.file_data_hash,
            file_meta=dict()
        )
        result: Result[FileDocumentResponse] = Result(
            status_code=status.HTTP_201_CREATED,
            message="FileDocumentManagement.create_one: Succeed.",
            data=file_document_response,
        )
        return result

    async def create_one_raw(self, state: State, file_document_creator: FileDocument, file_data: bytes) -> Result[
        FileDocumentResponse]:
        created_file_document: FileDocument = await self.file_document_repository.create_one(
            session=state.session,
            file_document_creator=file_document_creator,
            file_data=file_data
        )
        result: Result[FileDocumentResponse] = Result(
            status_code=status.HTTP_201_CREATED,
            message="FileDocumentManagement.create_one_raw: Succeed.",
            data=created_file_document,
        )
        return result

    async def patch_one_by_id(self, state: State, id: UUID, body: PatchOneBody) -> Result[
        FileDocumentResponse]:
        try:
            document_patcher: Document = Document(
                id=id,
                name=body.document_name,
                description=body.document_description,
                document_type_id=body.document_type_id,
                account_id=body.document_account_id
            )
            patched_document: Result[Document] = await self.document_management.patch_one_by_id_raw(
                state=state,
                id=id,
                document_patcher=document_patcher
            )
            if patched_document.status_code != status.HTTP_200_OK:
                result: Result[FileDocumentResponse] = Result(
                    status_code=patched_document.status_code,
                    message=f"FileDocumentManagement.patch_one_by_id: Failed, {patched_document.message}",
                    data=None,
                )
                raise SessionMiddleware.HandlerException(
                    result=result
                )

            file_data: bytes = await body.file_data.read()
            await body.file_data.close()
            file_document_patcher: FileDocument = FileDocument(
                file_name=body.file_name,
                file_data_hash=hashlib.sha256(file_data).hexdigest()
            )
            patched_file_document: FileDocument = await self.file_document_repository.patch_one_by_id(
                session=state.session,
                id=id,
                file_document_patcher=file_document_patcher,
                file_data=file_data
            )
            patched_file_document_response: FileDocumentResponse = FileDocumentResponse(
                id=patched_document.data.id,
                document_name=patched_document.data.name,
                document_description=patched_document.data.description,
                document_type_id=patched_document.data.document_type_id,
                document_account_id=patched_document.data.account_id,
                file_name=patched_file_document.file_name,
                file_data_hash=patched_file_document.file_data_hash,
                file_meta=dict()
            )
            result: Result[FileDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="FileDocumentManagement.patch_one_by_id: Succeed.",
                data=patched_file_document_response,
            )
        except exc.NoResultFound:
            result: Result[FileDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="FileDocumentManagement.patch_one_by_id: Failed, file_document is not found.",
                data=None,
            )
        return result

    async def patch_one_by_id_raw(self, state: State, id: UUID, file_document_patcher: FileDocument,
                                  file_data: bytes) -> \
            Result[
                FileDocumentResponse]:
        patched_file_document: FileDocument = await self.file_document_repository.patch_one_by_id(
            session=state.session,
            id=id,
            file_document_patcher=file_document_patcher,
            file_data=file_data
        )
        result: Result[FileDocumentResponse] = Result(
            status_code=status.HTTP_200_OK,
            message="FileDocumentManagement.patch_one_by_id_raw: Succeed.",
            data=patched_file_document,
        )
        return result

    async def delete_one_by_id(self, state: State, id: UUID) -> Result[FileDocumentResponse]:
        try:
            deleted_file_document: FileDocument = await self.file_document_repository.delete_one_by_id(
                session=state.session,
                id=id
            )
            deleted_document: Result[Document] = await self.document_management.delete_one_by_id(
                state=state,
                id=id
            )
            if deleted_document.status_code != status.HTTP_200_OK:
                result: Result[FileDocumentResponse] = Result(
                    status_code=deleted_document.status_code,
                    message=f"FileDocumentManagement.delete_one_by_id: Failed, {deleted_document.message}",
                    data=None,
                )
                raise SessionMiddleware.HandlerException(
                    result=result
                )

            deleted_file_document_response: FileDocumentResponse = FileDocumentResponse(
                id=deleted_document.data.id,
                document_name=deleted_document.data.name,
                document_description=deleted_document.data.description,
                document_type_id=deleted_document.data.document_type_id,
                document_account_id=deleted_document.data.account_id,
                file_name=deleted_file_document.file_name,
                file_data_hash=deleted_file_document.file_data_hash,
                file_meta=dict()
            )
            result: Result[FileDocumentResponse] = Result(
                status_code=status.HTTP_200_OK,
                message="FileDocumentManagement.delete_one_by_id: Succeed.",
                data=deleted_file_document_response,
            )
        except exc.NoResultFound:
            result: Result[FileDocumentResponse] = Result(
                status_code=status.HTTP_404_NOT_FOUND,
                message="FileDocumentManagement.delete_one_by_id: Failed, file_document is not found.",
                data=None,
            )
        return result
