import base64
import os
import uuid
from pathlib import Path

from app.inners.models.entities.document import Document
from app.inners.models.entities.document_process import DocumentProcess
from app.inners.models.entities.document_type import DocumentType
from app.inners.models.value_objects.contracts.requests.managements.document_processes.create_one_request import \
    CreateOneRequest as DocumentProcessCreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.document_types.read_one_by_id_request import \
    ReadOneByIdRequest as DocumentTypeReadOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.documents.read_one_by_id_request import \
    ReadOneByIdRequest as DocumentReadOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.file_documents.create_body import \
    CreateBody as FileDocumentCreateBody
from app.inners.models.value_objects.contracts.requests.managements.file_documents.create_one_request import \
    CreateOneRequest as FileDocumentCreateOneRequest
from app.inners.models.value_objects.contracts.requests.passage_searches.process_body import ProcessBody
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.managements.documents.document_response import DocumentResponse
from app.inners.use_cases.document_conversion.base_document_conversion import BaseDocumentConversion
from app.inners.use_cases.managements.document_management import DocumentManagement
from app.inners.use_cases.managements.document_process_management import DocumentProcessManagement
from app.inners.use_cases.managements.document_type_management import DocumentTypeManagement
from app.inners.use_cases.managements.file_document_management import FileDocumentManagement
from app.inners.use_cases.managements.text_document_management import TextDocumentManagement
from app.inners.use_cases.managements.web_document_management import WebDocumentManagement
from app.inners.use_cases.utilities.annotater import Annotater
from app.inners.use_cases.utilities.document_conversion_utility import DocumentConversionUtility
from app.inners.use_cases.utilities.document_processor_utility import DocumentProcessorUtility
from app.inners.use_cases.utilities.search_statistic import SearchStatistic
from app.outers.settings.temp_datastore_setting import TempDatastoreSetting


class PassageSearchDocumentConversion(BaseDocumentConversion):

    def __init__(
            self,
            document_management: DocumentManagement,
            document_type_management: DocumentTypeManagement,
            file_document_management: FileDocumentManagement,
            text_document_management: TextDocumentManagement,
            web_document_management: WebDocumentManagement,
            temp_datastore_setting: TempDatastoreSetting,
            document_conversion_utility: DocumentConversionUtility,
            document_process_management: DocumentProcessManagement,
            search_statistics: SearchStatistic,
            document_processor_utility: DocumentProcessorUtility,
            annotater: Annotater
    ):
        super().__init__(
            document_management,
            document_type_management,
            file_document_management,
            text_document_management,
            web_document_management,
            temp_datastore_setting,
            document_conversion_utility
        )
        self.document_process_management = document_process_management
        self.search_statistics = search_statistics
        self.document_processor_utility = document_processor_utility
        self.annotater = annotater

    async def convert_retrieval_result_to_highlighted_pdf(
            self,
            process_body: ProcessBody,
            retrieval_result: dict
    ) -> bytes:
        found_document: Content[Document] = await self.document_management.read_one_by_id(
            request=DocumentReadOneByIdRequest(
                id=process_body.input_setting.document_setting.document_id
            )
        )

        found_document_type: Content[DocumentType] = await self.document_type_management.read_one_by_id(
            request=DocumentTypeReadOneByIdRequest(
                id=found_document.data.document_type_id
            )
        )

        corpus: str = await self.convert_document_to_corpus(
            document_setting_body=process_body.input_setting.document_setting,
            document=found_document.data,
            document_type=found_document_type.data
        )

        result_windowed_documents: list = retrieval_result["documents"]
        result_documents = self.document_processor_utility.granularize(
            corpus=corpus,
            corpus_source_type=found_document_type.data.name,
            granularity=process_body.input_setting.granularity
        )

        result_document_indexes_with_overlapped_scores: dict[int, dict] = \
            self.search_statistics.get_document_indexes_with_overlapped_scores(result_windowed_documents)

        selected_result_labels: list = self.search_statistics.get_selected_labels(
            document_indexes_with_overlapped_scores=result_document_indexes_with_overlapped_scores,
            top_k=process_body.input_setting.ranker.top_k,
        )
        selected_result_documents: list[str] = self.search_statistics.get_selected_documents(
            document_indexes_with_overlapped_scores=result_document_indexes_with_overlapped_scores,
            top_k=process_body.input_setting.ranker.top_k,
            source_documents=result_documents
        )

        pdf_output_file_bytes: bytes = self.document_conversion_utility.corpus_to_pdf(
            corpus=corpus,
            document=found_document.data,
            document_type=found_document_type.data,
        )
        highlighted_pdf_output_file_bytes: bytes = self.annotater.annotate(
            labels=selected_result_labels,
            documents=selected_result_documents,
            input_file_bytes=base64.b64decode(pdf_output_file_bytes)
        )

        if found_document_type.data.name == "file":
            os.remove(Path(corpus))

        return highlighted_pdf_output_file_bytes

    async def convert_retrieval_result_to_document(
            self,
            process_body: ProcessBody,
            retrieval_result: dict,
            process_duration: float
    ) -> DocumentResponse:
        found_document_type_output: Content[DocumentType] = await self.document_type_management.read_one_by_id(
            request=DocumentTypeReadOneByIdRequest(
                id=process_body.output_setting.document_type_id
            )
        )

        document_process_to_create: DocumentProcess = DocumentProcess(
            id=uuid.uuid4(),
            initial_document_id=process_body.input_setting.document_setting.document_id,
            final_document_id=uuid.uuid4(),
            process_duration=process_duration,
        )

        if found_document_type_output.data.name == "file":
            document_response: Content[DocumentResponse] = await self.file_document_management.create_one(
                request=FileDocumentCreateOneRequest(
                    body=FileDocumentCreateBody(
                        id=document_process_to_create.final_document_id,
                        name=f"output",
                        description=f"document process id: {document_process_to_create.id}",
                        document_type_id=found_document_type_output.data.id,
                        account_id=process_body.account_id,
                        file_name=f"output",
                        file_extension=".pdf",
                        file_bytes=await self.convert_retrieval_result_to_highlighted_pdf(
                            process_body=process_body,
                            retrieval_result=retrieval_result
                        )
                    )
                )
            )
        else:
            raise NotImplementedError(f"Document type {found_document_type_output.data.name} is not supported.")

        created_document_process = await self.document_process_management.create_one(
            request=DocumentProcessCreateOneRequest(
                body=document_process_to_create
            )
        )

        return document_response.data
