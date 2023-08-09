from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.inners.use_cases.document_conversion.long_form_qa_document_conversion import LongFormQADocumentConversion
from app.inners.use_cases.document_conversion.passage_search_document_conversion import PassageSearchDocumentConversion
from app.outers.containers.setting_container import SettingContainer
from app.outers.containers.use_cases.management_container import ManagementContainer
from app.outers.containers.use_cases.utility_container import UtilityContainer


class DocumentConversionContainer(DeclarativeContainer):
    settings: SettingContainer = providers.DependenciesContainer()
    utilities: UtilityContainer = providers.DependenciesContainer()
    managements: ManagementContainer = providers.DependenciesContainer()

    long_form_qa_document_conversion: LongFormQADocumentConversion = providers.Singleton(
        LongFormQADocumentConversion,
        document_management=managements.document,
        document_type_management=managements.document_type,
        file_document_management=managements.file_document,
        text_document_management=managements.text_document,
        web_document_management=managements.web_document,
        temp_persistence_setting=settings.temp_persistence,
        document_conversion_utility=utilities.document_conversion,
        search_statistics=utilities.search_statistic,
        document_processor_utility=utilities.document_processor,
        document_process_management=managements.document_process,
    )
    passage_search_document_conversion: PassageSearchDocumentConversion = providers.Singleton(
        PassageSearchDocumentConversion,
        document_management=managements.document,
        document_type_management=managements.document_type,
        file_document_management=managements.file_document,
        text_document_management=managements.text_document,
        web_document_management=managements.web_document,
        temp_persistence_setting=settings.temp_persistence,
        document_conversion_utility=utilities.document_conversion,
        document_process_management=managements.document_process,
        search_statistics=utilities.search_statistic,
        document_processor_utility=utilities.document_processor,
        annotater=utilities.annotater,
    )
