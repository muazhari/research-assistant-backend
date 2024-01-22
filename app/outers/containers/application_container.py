from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.outers.containers.datastore_container import DatastoreContainer
from app.outers.containers.gateway_container import GatewayContainer
from app.outers.containers.repository_container import RepositoryContainer
from app.outers.containers.setting_container import SettingContainer
from app.outers.containers.use_case_container import UseCaseContainer


class ApplicationContainer(DeclarativeContainer):
    settings: SettingContainer = providers.Container(
        SettingContainer
    )

    datastores: DatastoreContainer = providers.Container(
        DatastoreContainer,
        settings=settings
    )

    repositories: RepositoryContainer = providers.Container(
        RepositoryContainer,
        settings=settings,
        datastores=datastores
    )

    gateways: GatewayContainer = providers.Container(
        GatewayContainer,
        settings=settings
    )

    use_cases: UseCaseContainer = providers.Container(
        UseCaseContainer,
        settings=settings,
        repositories=repositories,
        gateways=gateways,
    )
