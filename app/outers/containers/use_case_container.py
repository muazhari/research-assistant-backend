from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.outers.containers.use_cases.authentication_container import AuthenticationContainer
from app.outers.containers.use_cases.authorization_container import AuthorizationContainer
from app.outers.containers.use_cases.longform_qa_container import LongFormQAContainer
from app.outers.containers.use_cases.management_container import ManagementContainer
from app.outers.containers.use_cases.passage_search_container import PassageSearchContainer
from app.outers.containers.use_cases.utility_container import UtilityContainer


class UseCaseContainer(DeclarativeContainer):
    settings = providers.DependenciesContainer()
    datastores = providers.DependenciesContainer()
    repositories = providers.DependenciesContainer()
    gateways = providers.DependenciesContainer()

    utilities = providers.Container(
        UtilityContainer,
        settings=settings
    )
    managements = providers.Container(
        ManagementContainer,
        repositories=repositories,
    )
    authentications = providers.Container(
        AuthenticationContainer,
        managements=managements,
    )
    authorizations = providers.Container(
        AuthorizationContainer,
        managements=managements,
    )
    passage_searches = providers.Container(
        PassageSearchContainer,
        settings=settings,
        datastores=datastores,
        utilities=utilities,
        managements=managements,
    )
    longform_qas = providers.Container(
        LongFormQAContainer,
        settings=settings,
        datastores=datastores,
        utilities=utilities,
        managements=managements,
    )
