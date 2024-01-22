from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.outers.containers.setting_container import SettingContainer
from app.outers.datastores.one_datastore import OneDatastore


class DatastoreContainer(DeclarativeContainer):
    settings: SettingContainer = providers.DependenciesContainer()

    one_datastore: OneDatastore = providers.Singleton(
        OneDatastore,
        one_datastore_setting=settings.one_datastore_setting
    )
