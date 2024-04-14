from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.inners.use_cases.passage_searches.process_passage_search import ProcessPassageSearch


class PassageSearchContainer(DeclarativeContainer):
    graphs = providers.DependenciesContainer()
    managements = providers.DependenciesContainer()
    document_converter = providers.DependenciesContainer()

    process = providers.Singleton(
        ProcessPassageSearch,
        passage_search_graph=graphs.passage_search,
        file_document_management=managements.file_document,
        document_process_management=managements.document_process,
        libre_office_document_converter=document_converter.libre_office,
        marker_document_converter=document_converter.marker,
    )
