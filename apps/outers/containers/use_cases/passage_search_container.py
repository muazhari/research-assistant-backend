from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.inners.use_cases.passage_searches.process_passage_search import ProcessPassageSearch


class PassageSearchContainer(DeclarativeContainer):
    graphs = providers.DependenciesContainer()

    process = providers.Singleton(
        ProcessPassageSearch,
        passage_search_graph=graphs.passage_search,
    )
