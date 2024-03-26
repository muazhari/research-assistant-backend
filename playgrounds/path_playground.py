import os
import pathlib
from pathlib import Path

import torch

from apps.outers.settings.temp_datastore_setting import TempDatastoreSetting

print(torch.cuda.is_available())

temp_datastore_setting = TempDatastoreSetting()
file_path_1 = temp_datastore_setting.TEMP_DATASTORE_PATH / Path("__init__.py")
file_path_2 = temp_datastore_setting.TEMP_DATASTORE_PATH / "__init__.py"
file_path_3 = temp_datastore_setting.TEMP_DATASTORE_PATH.joinpath(Path("__init__.py"))
print(temp_datastore_setting.TEMP_DATASTORE_PATH.exists())
print(temp_datastore_setting.TEMP_DATASTORE_PATH)
print(file_path_1)
print(file_path_2)
print(file_path_3)
print(file_path_1 == file_path_2 == file_path_3)
print(file_path_1.exists())
print(file_path_2.exists())
print(file_path_3.exists())

file_path_4 = pathlib.Path()
print(file_path_4)

file_path_5 = pathlib.Path(os.getcwd())
print(file_path_5)
file_path_6 = file_path_5 / file_path_1
print(file_path_6)
print(file_path_6.exists())

file_path_7 = pathlib.Path("/mnt/c/Data/Apps/research-assistant-infrastructure/data/models/infloat/multilingual-e5-large-instruct")
print(file_path_7)
print(file_path_7.exists())