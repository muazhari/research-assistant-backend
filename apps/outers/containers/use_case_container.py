from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.outers.containers.use_cases.authentication_container import AuthenticationContainer
from apps.outers.containers.use_cases.authorization_container import AuthorizationContainer
from apps.outers.containers.use_cases.document_converter_container import DocumentConverterContainer
from apps.outers.containers.use_cases.document_processor_container import DocumentProcessorContainer
from apps.outers.containers.use_cases.graph_container import GraphContainer
from apps.outers.containers.use_cases.long_form_qa_container import LongFormQAContainer
from apps.outers.containers.use_cases.management_container import ManagementContainer
from apps.outers.containers.use_cases.passage_search_container import PassageSearchContainer
from apps.outers.containers.use_cases.utility_container import UtilityContainer


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
    document_converter = providers.Container(
        DocumentConverterContainer,
        repositories=repositories,
    )
    document_processor = providers.Container(
        DocumentProcessorContainer,
        managements=managements,
    )
    graphs = providers.Container(
        GraphContainer,
        settings=settings,
        datastores=datastores,
        document_processors=document_processor,
    )
    passage_searches = providers.Container(
        PassageSearchContainer,
        graphs=graphs,
        managements=managements,
        document_converter=document_converter,
    )
    long_form_qas = providers.Container(
        LongFormQAContainer,
        graphs=graphs,
    )
