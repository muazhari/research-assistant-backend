from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.outers.datastores.one_datastore import OneDatastore


class DatastoreContainer(DeclarativeContainer):
    settings = providers.DependenciesContainer()

    one_datastore = providers.Singleton(
        OneDatastore,
        one_datastore_setting=settings.one_datastore_setting
    )
