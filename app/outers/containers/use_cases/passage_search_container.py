from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.inners.use_cases.passage_searches.passage_search import PassageSearch


class PassageSearchContainer(DeclarativeContainer):
    settings = providers.DependenciesContainer()
    datastores = providers.DependenciesContainer()
    utilities = providers.DependenciesContainer()
    managements = providers.DependenciesContainer()

    passage_search = providers.Singleton(
        PassageSearch,
    )
