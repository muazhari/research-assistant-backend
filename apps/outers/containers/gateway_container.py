from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer


class GatewayContainer(DeclarativeContainer):
    settings = providers.DependenciesContainer()
