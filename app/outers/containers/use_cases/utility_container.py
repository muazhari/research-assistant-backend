from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.inners.use_cases.utilities.annotater import Annotater
from app.inners.use_cases.utilities.document_conversion_utility import DocumentConversionUtility
from app.inners.use_cases.utilities.document_processor_utility import DocumentProcessorUtility
from app.inners.use_cases.utilities.management_utility import ManagementUtility
from app.inners.use_cases.utilities.query_processor_utility import QueryProcessorUtility
from app.inners.use_cases.utilities.search_statistic import SearchStatistic
from app.outers.containers.setting_container import SettingContainer


class UtilityContainer(DeclarativeContainer):
    settings: SettingContainer = providers.DependenciesContainer()

    document_conversion = providers.Singleton(
        DocumentConversionUtility
    )
    query_processor = providers.Singleton(
        QueryProcessorUtility,
    )
    document_processor = providers.Singleton(
        DocumentProcessorUtility,
        document_conversion_utility=document_conversion,
        temp_datastore_setting=settings.temp_datastore_setting
    )
    management = providers.Singleton(
        ManagementUtility
    )
    annotater: Annotater = providers.Singleton(
        Annotater,
        temp_datastore_setting=settings.temp_datastore_setting,
    )
    search_statistic = providers.Singleton(
        SearchStatistic
    )
