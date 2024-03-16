from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer


class DocumentConversionContainer(DeclarativeContainer):
    settings = providers.DependenciesContainer()
    utilities = providers.DependenciesContainer()
    managements = providers.DependenciesContainer()
