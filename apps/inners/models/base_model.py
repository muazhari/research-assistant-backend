from pydantic import BaseModel as PydanticBaseModelV2
from pydantic.v1 import BaseModel as PydanticBaseModelV1


class BaseModel:
    def patch_from(self, patcher: dict):
        for key, value in patcher.items():
            if not hasattr(self, key):
                raise ValueError(f"Attribute {key} not found in {self.__class__.__name__}.")
            self.__setattr__(key, value)
        return self


class BaseModelV1(PydanticBaseModelV1, BaseModel):
    class Config:
        arbitrary_types_allowed = True
        validate_all = True
        validate_assignment = True


class BaseModelV2(PydanticBaseModelV2, BaseModel):
    class Config:
        arbitrary_types_allowed = True
        revalidate_instances = "always"
        validate_default = True
        validate_return = True
        validate_assignment = True
