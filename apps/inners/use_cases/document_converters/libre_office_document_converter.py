import subprocess
from pathlib import Path
from uuid import UUID

import pdfkit
from starlette.datastructures import State

from apps.inners.exceptions import use_case_exception
from apps.inners.models.daos.document import Document
from apps.inners.models.daos.file_document import FileDocument
from apps.inners.models.daos.text_document import TextDocument
from apps.inners.models.daos.web_document import WebDocument
from apps.inners.models.dtos.constants.document_type_constant import DocumentTypeConstant
from apps.outers.repositories.document_repository import DocumentRepository
from apps.outers.repositories.file_document_repository import FileDocumentRepository
from apps.outers.repositories.text_document_repository import TextDocumentRepository
from apps.outers.repositories.web_document_repository import WebDocumentRepository


class LibreOfficeDocumentConverter:
    def __init__(
            self,
            document_repository: DocumentRepository,
            file_document_repository: FileDocumentRepository,
            text_document_repository: TextDocumentRepository,
            web_document_repository: WebDocumentRepository,
    ):
        self.document_repository = document_repository
        self.file_document_repository = file_document_repository
        self.text_document_repository = text_document_repository
        self.web_document_repository = web_document_repository
        self.file_path: Path = self.file_document_repository.file_path / "libre_office_converted_documents"
        self.file_path.mkdir(exist_ok=True)
        self.pdf_options = {
            'page-size': 'Letter',
            'margin-top': '0.25in',
            'margin-right': '1.00in',
            'margin-bottom': '0.25in',
            'margin-left': '1.00in',
        }

    async def convert_from_data(self, input_file_data: bytes, input_format: str, output_format: str) -> bytes:
        id: UUID = UUID(int=0)
        input_file_path: Path = self.file_path / f"{id}.{input_format}"
        self.file_document_repository.save_file(
            relative_file_path=Path(input_file_path.parent.name) / input_file_path.name,
            file_data=input_file_data
        )
        command: str = f"libreoffice --headless --convert-to {output_format} --outdir {self.file_path} {self.file_path / input_file_path.name}"
        subprocess.run(command, shell=True)
        output_file_path: Path = self.file_path / f"{id}.{output_format}"
        output_file_data: bytes = self.file_document_repository.read_file_data(
            relative_file_path=Path(output_file_path.parent.name) / output_file_path.name
        )
        self.file_document_repository.remove_file(
            relative_file_path=Path(input_file_path.parent.name) / input_file_path.name
        )
        self.file_document_repository.remove_file(
            relative_file_path=Path(output_file_path.parent.name) / output_file_path.name
        )

        return output_file_data

    async def convert_from_document_id(self, state: State, document_id: UUID, output_format: str) -> bytes:
        found_document: Document = await self.document_repository.find_one_by_id_and_accound_id(
            session=state.session,
            id=document_id,
            account_id=state.authorized_session.account_id
        )
        if found_document.document_type_id == DocumentTypeConstant.FILE:
            found_file_document: FileDocument = await self.file_document_repository.find_one_by_id_and_account_id(
                session=state.session,
                id=document_id,
                account_id=state.authorized_session.account_id
            )
            input_file_path: Path = Path(self.file_path.name) / found_file_document.file_name
            file_data: bytes = self.file_document_repository.get_object_data(
                object_name=found_file_document.file_name
            )
            self.file_document_repository.save_file(
                relative_file_path=input_file_path,
                file_data=file_data
            )
        elif found_document.document_type_id == DocumentTypeConstant.TEXT:
            found_text_document: TextDocument = await self.text_document_repository.find_one_by_id_and_account_id(
                session=state.session,
                id=document_id,
                account_id=state.authorized_session.account_id
            )
            input_file_path: Path = Path(self.file_path.name) / f"{document_id}.txt"
            self.file_document_repository.save_file(
                relative_file_path=input_file_path,
                file_data=found_text_document.text_content.encode()
            )
        elif found_document.document_type_id == DocumentTypeConstant.WEB:
            found_web_document: WebDocument = await self.web_document_repository.find_one_by_id_and_account_id(
                session=state.session,
                id=document_id,
                account_id=state.authorized_session.account_id
            )
            input_file_path: Path = Path(self.file_path.name) / f"{document_id}.pdf"
            self.file_document_repository.save_file(
                relative_file_path=input_file_path,
                file_data=pdfkit.from_url(found_web_document.web_url, False, options=self.pdf_options)
            )
        else:
            raise use_case_exception.DocumentTypeNotSupported()

        if input_file_path.suffix[1:] == output_format:
            output_file_data: bytes = self.file_document_repository.read_file_data(
                relative_file_path=input_file_path
            )
            self.file_document_repository.remove_file(
                relative_file_path=input_file_path
            )

            return output_file_data

        command: str = f"libreoffice --headless --convert-to {output_format} --outdir {self.file_path} {self.file_path / input_file_path.name}"
        subprocess.run(command, shell=True)
        output_file_path: Path = Path(self.file_path.name) / f"{input_file_path.stem}.{output_format}"
        output_file_data: bytes = self.file_document_repository.read_file_data(
            relative_file_path=output_file_path
        )
        self.file_document_repository.remove_file(
            relative_file_path=input_file_path
        )
        self.file_document_repository.remove_file(
            relative_file_path=output_file_path
        )

        return output_file_data
