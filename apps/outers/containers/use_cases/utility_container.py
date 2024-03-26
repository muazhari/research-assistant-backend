from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.inners.use_cases.utilities.annotater import Annotater
from apps.inners.use_cases.utilities.search_statistic import SearchStatistic


class UtilityContainer(DeclarativeContainer):
    settings = providers.DependenciesContainer()

    annotater = providers.Singleton(
        Annotater,
        temp_datastore_setting=settings.temp_datastore_setting,
    )
    search_statistic = providers.Singleton(
        SearchStatistic
    )
