from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.outers.datastores.four_datastore import FourDatastore
from apps.outers.datastores.one_datastore import OneDatastore
from apps.outers.datastores.temp_datastore import TempDatastore
from apps.outers.datastores.three_datastore import ThreeDatastore
from apps.outers.datastores.two_datastore import TwoDatastore


class DatastoreContainer(DeclarativeContainer):
    settings = providers.DependenciesContainer()

    temp = providers.Singleton(
        TempDatastore,
        temp_datastore_setting=settings.temp_datastore
    )
    one = providers.Singleton(
        OneDatastore,
        one_datastore_setting=settings.one_datastore
    )
    two = providers.Singleton(
        TwoDatastore,
        two_datastore_setting=settings.two_datastore
    )
    three = providers.Singleton(
        ThreeDatastore,
        three_datastore_setting=settings.three_datastore
    )
    four = providers.Singleton(
        FourDatastore,
        four_datastore_setting=settings.four_datastore
    )
