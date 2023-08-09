from typing import Dict

from app.inners.models.entities.base_entity import BaseEntity


class ManagementUtility:

    def filter(self, query_parameter: Dict[str, str], entity: BaseEntity) -> bool:
        for key in query_parameter.keys():
            if key not in entity.dict().keys():
                return False
            if query_parameter[key] == str(entity.dict()[key]):
                return True
        return False
