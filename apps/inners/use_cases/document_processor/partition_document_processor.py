import io
import shutil
from pathlib import Path
from typing import List
from uuid import UUID

from pypdf import PdfReader, PdfWriter
from starlette.datastructures import State
from unstructured.documents.elements import Element
from unstructured.partition.auto import partition
from unstructured.partition.html import partition_html
from unstructured.partition.text import partition_text
from unstructured.partition.utils.constants import PartitionStrategy

from apps.inners.exceptions import use_case_exception
from apps.inners.models.daos.document import Document
from apps.inners.models.dtos.constants.document_type_constant import DocumentTypeConstant
from apps.inners.models.dtos.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from apps.inners.models.dtos.contracts.responses.managements.documents.text_document_response import \
    TextDocumentResponse
from apps.inners.models.dtos.contracts.responses.managements.documents.web_document_response import WebDocumentResponse
from apps.inners.use_cases.managements.document_management import DocumentManagement
from apps.inners.use_cases.managements.file_document_management import FileDocumentManagement
from apps.inners.use_cases.managements.text_document_management import TextDocumentManagement
from apps.inners.use_cases.managements.web_document_management import WebDocumentManagement


class PartitionDocumentProcessor:
    def __init__(
            self,
            document_management: DocumentManagement,
            file_document_management: FileDocumentManagement,
            text_document_management: TextDocumentManagement,
            web_document_management: WebDocumentManagement,
    ):
        self.document_management = document_management
        self.file_document_management = file_document_management
        self.text_document_management = text_document_management
        self.web_document_management = web_document_management

    @staticmethod
    def split_pdf_page(file_data: bytes, start_page: int, end_page: int) -> bytes:
        input_file_io = io.BytesIO(file_data)
        input_pdf_reader = PdfReader(input_file_io)
        output_pdf_writer = PdfWriter()
        for page in input_pdf_reader.pages[start_page - 1:end_page]:
            output_pdf_writer.add_page(page)
        output_file_io = io.BytesIO()
        output_pdf_writer.write(output_file_io)
        output_file_data = output_file_io.getvalue()
        input_file_io.close()
        output_file_io.close()

        return output_file_data

    async def partition_file(self, state: State, found_document: Document,
                             partition_strategy: str = PartitionStrategy.AUTO) -> List[Element]:
        found_file_document: FileDocumentResponse = await self.file_document_management.find_one_by_id_with_authorization(
            state=state,
            id=found_document.id
        )
        file_data: bytes = self.file_document_management.file_document_repository.get_object_data(
            object_name=found_file_document.file_name
        )
        extracted_image_path: Path = self.file_document_management.file_document_repository.file_path / "assets" / found_file_document.file_data_hash
        extracted_image_path.mkdir(exist_ok=True, parents=True)
        shutil.rmtree(extracted_image_path)
        elements: List[Element] = partition(
            file=io.BytesIO(file_data),
            extract_image_block_types=["Image"],
            extract_image_block_output_dir=str(extracted_image_path),
            strategy=partition_strategy,
            hi_res_model_name="yolox",
        )

        return elements

    async def partition_text(self, state: State, found_document: Document) -> List[Element]:
        found_text_document: TextDocumentResponse = await self.text_document_management.find_one_by_id_with_authorization(
            state=state,
            id=found_document.id
        )
        elements: List[Element] = partition_text(
            text=found_text_document.text_content,
        )

        return elements

    async def partition_web(self, state: State, found_document: Document) -> List[Element]:
        found_web_document: WebDocumentResponse = await self.web_document_management.find_one_by_id_with_authorization(
            state=state,
            id=found_document.id
        )
        elements: List[Element] = partition_html(
            url=found_web_document.web_url,
            ssl_verify=False
        )

        return elements

    async def partition(self, state: State, document_id: UUID, file_partition_strategy: str) -> List[Element]:
        found_document: Document = await self.document_management.find_one_by_id_with_authorization(
            state=state,
            id=document_id
        )
        if found_document.document_type_id == DocumentTypeConstant.FILE:
            elements: List[Element] = await self.partition_file(
                state=state,
                found_document=found_document,
                partition_strategy=file_partition_strategy
            )
        elif found_document.document_type_id == DocumentTypeConstant.TEXT:
            elements: List[Element] = await self.partition_text(
                state=state,
                found_document=found_document
            )
        elif found_document.document_type_id == DocumentTypeConstant.WEB:
            elements: List[Element] = await self.partition_web(
                state=state,
                found_document=found_document
            )
        else:
            raise use_case_exception.DocumentTypeNotSupported()

        return elements
