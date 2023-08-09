from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.inners.use_cases.utilities.annotater import Annotater
from app.inners.use_cases.utilities.document_conversion_utility import DocumentConversionUtility
from app.inners.use_cases.utilities.document_processor_utility import DocumentProcessorUtility
from app.inners.use_cases.utilities.management_utility import ManagementUtility
from app.inners.use_cases.utilities.search_statistic import SearchStatistic
from app.outers.containers.repository_container import RepositoryContainer
from app.outers.containers.setting_container import SettingContainer


class UtilityContainer(DeclarativeContainer):
    settings: SettingContainer = providers.DependenciesContainer()
    repositories: RepositoryContainer = providers.DependenciesContainer()

    document_conversion = providers.Singleton(
        DocumentConversionUtility
    )
    document_processor = providers.Singleton(
        DocumentProcessorUtility,
        document_conversion_utility=document_conversion,
        temp_persistence_setting=settings.temp_persistence
    )
    management = providers.Singleton(
        ManagementUtility
    )
    annotater: Annotater = providers.Singleton(
        Annotater,
        temp_persistence_setting=settings.temp_persistence,
    )
    search_statistic = providers.Singleton(
        SearchStatistic
    )
