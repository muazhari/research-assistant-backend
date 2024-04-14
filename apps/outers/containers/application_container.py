from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.outers.containers.controller_container import ControllerContainer
from apps.outers.containers.datastore_container import DatastoreContainer
from apps.outers.containers.gateway_container import GatewayContainer
from apps.outers.containers.repository_container import RepositoryContainer
from apps.outers.containers.router_container import RouterContainer
from apps.outers.containers.setting_container import SettingContainer
from apps.outers.containers.use_case_container import UseCaseContainer


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
        datastores=datastores,
        repositories=repositories,
        gateways=gateways,
    )
    controllers = providers.Container(
        ControllerContainer,
        managements=use_cases.managements,
        authentications=use_cases.authentications,
        authorizations=use_cases.authorizations,
        passage_searches=use_cases.passage_searches,
        long_form_qas=use_cases.long_form_qas,
    )
    routers = providers.Container(
        RouterContainer,
        controllers=controllers
    )
