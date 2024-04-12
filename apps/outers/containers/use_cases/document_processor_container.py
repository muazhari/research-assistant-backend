from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.inners.use_cases.document_processor.category_document_processor import CategoryDocumentProcessor
from apps.inners.use_cases.document_processor.partition_document_processor import PartitionDocumentProcessor
from apps.inners.use_cases.document_processor.summary_document_processor import SummaryDocumentProcessor


class DocumentProcessorContainer(DeclarativeContainer):
    managements = providers.DependenciesContainer()

    partition = providers.Singleton(
        PartitionDocumentProcessor,
        document_management=managements.document,
        file_document_management=managements.file_document,
        text_document_management=managements.text_document,
        web_document_management=managements.web_document
    )
    summary = providers.Singleton(
        SummaryDocumentProcessor,
    )
    category = providers.Singleton(
        CategoryDocumentProcessor,
        summary_document_processor=summary
    )
