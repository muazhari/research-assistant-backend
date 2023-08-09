from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.outers.containers.setting_container import SettingContainer
from app.outers.persistences.datastore_one_persistence import DatastoreOnePersistence


class PersistenceContainer(DeclarativeContainer):
    settings: SettingContainer = providers.DependenciesContainer()

    datastore_one: DatastoreOnePersistence = providers.Singleton(
        DatastoreOnePersistence,
        datastore_one_setting=settings.datastore_one
    )
