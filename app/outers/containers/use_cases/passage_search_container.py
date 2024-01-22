from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.inners.use_cases.passage_search.passage_search import PassageSearch
from app.inners.use_cases.passage_search.ranker_model import RankerModel
from app.inners.use_cases.passage_search.retriever_model import RetrieverModel
from app.outers.containers.setting_container import SettingContainer
from app.outers.containers.use_cases.document_conversion_container import DocumentConversionContainer
from app.outers.containers.use_cases.management_container import ManagementContainer
from app.outers.containers.use_cases.utility_container import UtilityContainer


class PassageSearchContainer(DeclarativeContainer):
    settings: SettingContainer = providers.DependenciesContainer()
    utilities: UtilityContainer = providers.DependenciesContainer()
    managements: ManagementContainer = providers.DependenciesContainer()
    document_conversions: DocumentConversionContainer = providers.DependenciesContainer()

    retriever_model = providers.Singleton(
        RetrieverModel
    )
    ranker_model = providers.Singleton(
        RankerModel
    )
    passage_search: PassageSearch = providers.Singleton(
        PassageSearch,
        document_management=managements.document,
        document_type_management=managements.document_type,
        retriever_model=retriever_model,
        ranker_model=ranker_model,
        passage_search_document_conversion=document_conversions.passage_search_document_conversion,
        query_processor_utility=utilities.query_processor,
        document_processor_utility=utilities.document_processor,
        one_datastore_setting=settings.one_datastore_setting,
        two_datastore_setting=settings.two_datastore_setting
    )
