from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.outers.containers.datastore_container import DatastoreContainer
from app.outers.containers.gateway_container import GatewayContainer
from app.outers.containers.middleware_container import MiddlewareContainer
from app.outers.containers.repository_container import RepositoryContainer
from app.outers.containers.setting_container import SettingContainer
from app.outers.containers.use_case_container import UseCaseContainer


class ApplicationContainer(DeclarativeContainer):
    settings = providers.Container(
        SettingContainer
    )
    gateways = providers.Container(
        GatewayContainer,
        settings=settings
    )
    datastores = providers.Container(
        DatastoreContainer,
        settings=settings
    )
    repositories = providers.Container(
        RepositoryContainer,
        datastores=datastores
    )
    use_cases = providers.Container(
        UseCaseContainer,
        settings=settings,
        repositories=repositories,
        gateways=gateways,
    )
    middlewares = providers.Container(
        MiddlewareContainer,
        datastores=datastores
    )
