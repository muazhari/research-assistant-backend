from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.outers.containers.use_cases.authentication_container import AuthenticationContainer
from app.outers.containers.use_cases.document_conversion_container import DocumentConversionContainer
from app.outers.containers.use_cases.longform_qa_container import LongFormQAContainer
from app.outers.containers.use_cases.management_container import ManagementContainer
from app.outers.containers.use_cases.passage_search_container import PassageSearchContainer
from app.outers.containers.use_cases.utility_container import UtilityContainer


class UseCaseContainer(DeclarativeContainer):
    settings = providers.DependenciesContainer()
    repositories = providers.DependenciesContainer()
    gateways = providers.DependenciesContainer()

    utilities = providers.Container(
        UtilityContainer,
        settings=settings,
        repositories=repositories
    )
    managements = providers.Container(
        ManagementContainer,
        settings=settings,
        repositories=repositories,
        utilities=utilities
    )
    authentications = providers.Container(
        AuthenticationContainer,
        managements=managements,
    )
    document_conversions = providers.Container(
        DocumentConversionContainer,
        settings=settings,
        utilities=utilities,
        managements=managements
    )
    passage_searches = providers.Container(
        PassageSearchContainer,
        settings=settings,
        utilities=utilities,
        managements=managements,
        document_conversions=document_conversions,
    )
    longform_qas = providers.Container(
        LongFormQAContainer,
        settings=settings,
        utilities=utilities,
        managements=managements,
        document_conversions=document_conversions,
        passage_searches=passage_searches
    )
