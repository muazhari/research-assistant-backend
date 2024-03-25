from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.outers.datastores.four_datastore import FourDatastore
from app.outers.datastores.one_datastore import OneDatastore
from app.outers.datastores.three_datastore import ThreeDatastore
from app.outers.datastores.two_datastore import TwoDatastore


class DatastoreContainer(DeclarativeContainer):
    settings = providers.DependenciesContainer()

    one_datastore = providers.Singleton(
        OneDatastore,
        one_datastore_setting=settings.one_datastore_setting
    )
    two_datastore = providers.Singleton(
        TwoDatastore,
        two_datastore_setting=settings.two_datastore_setting
    )
    three_datastore = providers.Singleton(
        ThreeDatastore,
        three_datastore_setting=settings.three_datastore_setting
    )
    four_datastore = providers.Singleton(
        FourDatastore,
        four_datastore_setting=settings.four_datastore_setting
    )
