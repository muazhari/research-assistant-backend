from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.outers.settings.four_datastore_setting import FourDatastoreSetting
from app.outers.settings.one_datastore_setting import OneDatastoreSetting
from app.outers.settings.three_datastore_setting import ThreeDatastoreSetting
from app.outers.settings.two_datastore_setting import TwoDatastoreSetting


class SettingContainer(DeclarativeContainer):
    one_datastore_setting = providers.Singleton(
        OneDatastoreSetting
    )
    two_datastore_setting = providers.Singleton(
        TwoDatastoreSetting
    )
    three_datastore_setting = providers.Singleton(
        ThreeDatastoreSetting
    )
    four_datastore_setting = providers.Singleton(
        FourDatastoreSetting
    )
