from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.outers.settings.one_datastore_setting import OneDatastoreSetting


class SettingContainer(DeclarativeContainer):
    one_datastore_setting = providers.Singleton(OneDatastoreSetting)
