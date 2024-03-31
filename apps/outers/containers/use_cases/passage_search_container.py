from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.inners.use_cases.passage_searches.process_passage_search import ProcessPassageSearch


class PassageSearchContainer(DeclarativeContainer):
    settings = providers.DependenciesContainer()
    datastores = providers.DependenciesContainer()
    utilities = providers.DependenciesContainer()
    managements = providers.DependenciesContainer()

    process = providers.Singleton(
        ProcessPassageSearch,
    )
