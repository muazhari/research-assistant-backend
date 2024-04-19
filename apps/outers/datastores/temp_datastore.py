from apps.outers.settings.temp_datastore_setting import TempDatastoreSetting


class TempDatastore:

    def __init__(
            self,
            temp_datastore_setting: TempDatastoreSetting
    ):
        self.temp_datastore_setting = temp_datastore_setting
