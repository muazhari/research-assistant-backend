from pathlib import Path

import torch

from app.outers.settings.temp_persistence_setting import TempPersistenceSetting

print(torch.cuda.is_available())

temp_persistence_setting = TempPersistenceSetting()
file_path_1 = temp_persistence_setting.TEMP_PERSISTENCE_PATH / Path("__init__.py")
file_path_2 = temp_persistence_setting.TEMP_PERSISTENCE_PATH.joinpath(Path("__init__.py"))
print(file_path_1)
print(file_path_2)
print(file_path_1 == file_path_2)
print(file_path_1.exists())
print(file_path_2.exists())
