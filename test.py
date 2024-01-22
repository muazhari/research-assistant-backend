from pathlib import Path

import torch

from app.outers.settings.temp_datastore_setting import TempDatastoreSetting

print(torch.cuda.is_available())

temp_datastore_setting = TempDatastoreSetting()
file_path_1 = temp_datastore_setting.TEMP_DATASTORE_PATH / Path("__init__.py")
file_path_2 = temp_datastore_setting.TEMP_DATASTORE_PATH.joinpath(Path("__init__.py"))
print(file_path_1)
print(file_path_2)
print(file_path_1 == file_path_2)
print(file_path_1.exists())
print(file_path_2.exists())
