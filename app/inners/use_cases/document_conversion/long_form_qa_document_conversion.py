from app.inners.use_cases.document_conversion.base_document_conversion import BaseDocumentConversion
from app.inners.use_cases.managements.document_process_management import DocumentProcessManagement
from app.inners.use_cases.passage_search.search_statistics import SearchStatistics
from app.inners.use_cases.utilities.document_processor_utility import DocumentProcessorUtility


class LongFormQADocumentConversion(BaseDocumentConversion):

    def __init__(self):
        super().__init__()
        self.search_statistics = SearchStatistics()
        self.document_processor_utility = DocumentProcessorUtility()
        self.document_process_management = DocumentProcessManagement()
