from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.outers.settings.four_datastore_setting import FourDatastoreSetting
from apps.outers.settings.one_datastore_setting import OneDatastoreSetting
from apps.outers.settings.one_llm_setting import OneLlmSetting
from apps.outers.settings.temp_datastore_setting import TempDatastoreSetting
from apps.outers.settings.three_datastore_setting import ThreeDatastoreSetting
from apps.outers.settings.two_datastore_setting import TwoDatastoreSetting


class SettingContainer(DeclarativeContainer):
    one_llm = providers.Singleton(
        OneLlmSetting
    )
    temp_datastore = providers.Singleton(
        TempDatastoreSetting
    )
    one_datastore = providers.Singleton(
        OneDatastoreSetting
    )
    two_datastore = providers.Singleton(
        TwoDatastoreSetting
    )
    three_datastore = providers.Singleton(
        ThreeDatastoreSetting
    )
    four_datastore = providers.Singleton(
        FourDatastoreSetting
    )
