from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.inners.use_cases.long_form_qa.longform_qa import LongFormQA
from app.outers.containers.datastore_container import DatastoreContainer
from app.outers.containers.setting_container import SettingContainer
from app.outers.containers.use_cases.document_conversion_container import DocumentConversionContainer
from app.outers.containers.use_cases.management_container import ManagementContainer
from app.outers.containers.use_cases.passage_search_container import PassageSearchContainer
from app.outers.containers.use_cases.utility_container import UtilityContainer


class LongFormQAContainer(DeclarativeContainer):
    settings: SettingContainer = providers.DependenciesContainer()
    utilities: UtilityContainer = providers.DependenciesContainer()
    datastores: DatastoreContainer = providers.DependenciesContainer()
    managements: ManagementContainer = providers.DependenciesContainer()
    document_conversions: DocumentConversionContainer = providers.DependenciesContainer()
    passage_searches: PassageSearchContainer = providers.DependenciesContainer()

    longform_qa: LongFormQA = providers.Singleton(
        LongFormQA,
        passage_search=passage_searches.passage_search,
        long_form_qa_document_conversion=document_conversions.long_form_qa_document_conversion
    )
