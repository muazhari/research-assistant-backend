from pathlib import Path

import torch

from app.outers.settings.temp_persistence_setting import TempPersistenceSetting

print(torch.cuda.is_available())

temp_persistence_setting = TempPersistenceSetting()
print(temp_persistence_setting.TEMP_PERSISTENCE_PATH / Path("test.txt"))
print(temp_persistence_setting.TEMP_PERSISTENCE_PATH.joinpath(Path("test.txt")))
