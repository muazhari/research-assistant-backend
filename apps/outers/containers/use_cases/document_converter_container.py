from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.inners.use_cases.document_converters.libre_office_document_converter import LibreOfficeDocumentConverter
from apps.inners.use_cases.document_converters.marker_document_converter import MarkerDocumentConverter


class DocumentConverterContainer(DeclarativeContainer):
    repositories = providers.DependenciesContainer()

    libre_office = providers.Singleton(
        LibreOfficeDocumentConverter,
        document_repository=repositories.document,
        file_document_repository=repositories.file_document,
        text_document_repository=repositories.text_document,
        web_document_repository=repositories.web_document,
    )

    marker = providers.Singleton(
        MarkerDocumentConverter,
        file_document_repository=repositories.file_document,
    )
