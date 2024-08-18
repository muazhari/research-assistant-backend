from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.inners.use_cases.graphs.long_form_qa_graph import LongFormQaGraph
from apps.inners.use_cases.graphs.passage_search_graph import PassageSearchGraph


class GraphContainer(DeclarativeContainer):
    settings = providers.DependenciesContainer()
    datastores = providers.DependenciesContainer()
    document_processors = providers.DependenciesContainer()

    passage_search = providers.Singleton(
        PassageSearchGraph,
        one_llm_setting=settings.one_llm,
        two_llm_setting=settings.two_llm,
        two_datastore=datastores.two,
        four_datastore=datastores.four,
        partition_document_processor=document_processors.partition,
        category_document_processor=document_processors.category,
    )

    long_form_qa = providers.Singleton(
        LongFormQaGraph,
        one_llm_setting=settings.one_llm,
        two_llm_setting=settings.two_llm,
        two_datastore=datastores.two,
        four_datastore=datastores.four,
        partition_document_processor=document_processors.partition,
        category_document_processor=document_processors.category,
    )
