from app.inners.use_cases.document_conversion.base_document_conversion import BaseDocumentConversion
from app.inners.use_cases.managements.document_management import DocumentManagement
from app.inners.use_cases.managements.document_process_management import DocumentProcessManagement
from app.inners.use_cases.managements.document_type_management import DocumentTypeManagement
from app.inners.use_cases.managements.file_document_management import FileDocumentManagement
from app.inners.use_cases.managements.text_document_management import TextDocumentManagement
from app.inners.use_cases.managements.web_document_management import WebDocumentManagement
from app.inners.use_cases.utilities.document_conversion_utility import DocumentConversionUtility
from app.inners.use_cases.utilities.document_processor_utility import DocumentProcessorUtility
from app.inners.use_cases.utilities.search_statistic import SearchStatistic
from app.outers.settings.temp_persistence_setting import TempPersistenceSetting


class LongFormQADocumentConversion(BaseDocumentConversion):

    def __init__(
            self,
            document_management: DocumentManagement,
            document_type_management: DocumentTypeManagement,
            file_document_management: FileDocumentManagement,
            text_document_management: TextDocumentManagement,
            web_document_management: WebDocumentManagement,
            temp_persistence_setting: TempPersistenceSetting,
            document_conversion_utility: DocumentConversionUtility,
            search_statistics: SearchStatistic,
            document_processor_utility: DocumentProcessorUtility,
            document_process_management: DocumentProcessManagement
    ):
        super().__init__(
            document_management,
            document_type_management,
            file_document_management,
            text_document_management,
            web_document_management,
            temp_persistence_setting,
            document_conversion_utility
        )
        self.search_statistics = search_statistics
        self.document_processor_utility = document_processor_utility
        self.document_process_management = document_process_management
