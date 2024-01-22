from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.outers.settings.one_datastore_setting import OneDatastoreSetting
from app.outers.settings.openai_setting import OpenAiSetting
from app.outers.settings.temp_datastore_setting import TempDatastoreSetting
from app.outers.settings.two_datastore_setting import TwoDatastoreSetting


class SettingContainer(DeclarativeContainer):
    one_datastore_setting: OneDatastoreSetting = providers.Singleton(OneDatastoreSetting)
    two_datastore_setting: TwoDatastoreSetting = providers.Singleton(TwoDatastoreSetting)
    open_ai_setting: OpenAiSetting = providers.Singleton(OpenAiSetting)
    temp_datastore_setting: TempDatastoreSetting = providers.Singleton(TempDatastoreSetting)
