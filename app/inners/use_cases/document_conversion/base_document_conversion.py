import base64
import os
from pathlib import Path

from app.inners.models.entities.document import Document
from app.inners.models.entities.document_type import DocumentType
from app.inners.models.value_objects.contracts.requests.basic_settings.document_setting_body import DocumentSettingBody
from app.inners.models.value_objects.contracts.requests.managements.file_documents.read_one_by_id_request import \
    ReadOneByIdRequest as FileDocumentReadOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.text_documents.read_one_by_id_request import \
    ReadOneByIdRequest as TextDocumentReadOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.web_documents.read_one_by_id_request import \
    ReadOneByIdRequest as WebDocumentReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from app.inners.models.value_objects.contracts.responses.managements.documents.text_document_response import \
    TextDocumentResponse
from app.inners.models.value_objects.contracts.responses.managements.documents.web_document_response import \
    WebDocumentResponse
from app.inners.use_cases.managements.document_management import DocumentManagement
from app.inners.use_cases.managements.document_type_management import DocumentTypeManagement
from app.inners.use_cases.managements.file_document_management import FileDocumentManagement
from app.inners.use_cases.managements.text_document_management import TextDocumentManagement
from app.inners.use_cases.managements.web_document_management import WebDocumentManagement
from app.inners.use_cases.utilities.document_conversion_utility import DocumentConversionUtility
from app.outers.settings.temp_persistence_setting import TempPersistenceSetting


class BaseDocumentConversion:

    def __init__(self):

        self.document_management = DocumentManagement()
        self.document_type_management = DocumentTypeManagement()
        self.file_document_management = FileDocumentManagement()
        self.text_document_management = TextDocumentManagement()
        self.web_document_management = WebDocumentManagement()
        self.document_conversion_utility = DocumentConversionUtility()
        self.temp_persistence_setting = TempPersistenceSetting()

    async def convert_document_to_corpus(self, document_setting_body: DocumentSettingBody, document: Document,
                                         document_type: DocumentType) -> str:
        if document_type.name == "file":
            found_detail_document: Content[FileDocumentResponse] = await self.file_document_management.read_one_by_id(
                request=FileDocumentReadOneByIdRequest(
                    id=document.id
                )
            )
            file_extension: str = found_detail_document.data.file_extension

            if file_extension == ".pdf":
                new_file_name: str = f"{document.id}{file_extension}"
                file_path: Path = self.temp_persistence_setting.TEMP_PERSISTENCE_PATH / Path(new_file_name)
                file_bytes: bytes = base64.b64decode(found_detail_document.data.file_bytes)
                with open(file_path, "wb") as file:
                    file.write(file_bytes)
                corpus = file_path

                split_file_name: str = f"split_{document_setting_body.detail_setting.start_page}_to_{document_setting_body.detail_setting.end_page}_{new_file_name}"
                split_file_path: Path = self.temp_persistence_setting.TEMP_PERSISTENCE_PATH / Path(f"{split_file_name}")
                split_file_bytes: bytes = self.document_conversion_utility.split_pdf_page(
                    input_file_path=file_path,
                    output_file_path=split_file_path,
                    start_page=document_setting_body.detail_setting.start_page,
                    end_page=document_setting_body.detail_setting.end_page,
                )
                corpus = str(split_file_path)

                os.remove(file_path)
            else:
                raise NotImplementedError(f"File extension {file_extension} is not supported.")
        elif document_type.name == "text":
            found_detail_document: Content[TextDocumentResponse] = await self.text_document_management.read_one_by_id(
                request=TextDocumentReadOneByIdRequest(
                    id=document.id
                )
            )
            corpus = found_detail_document.data.text_content
        elif document_type.name == "web":
            found_detail_document: Content[WebDocumentResponse] = await self.web_document_management.read_one_by_id(
                request=WebDocumentReadOneByIdRequest(
                    id=document.id
                )
            )
            corpus = found_detail_document.data.web_url
        else:
            raise Exception(f"Document type {document_type.name} not yet supported.")

        return corpus
