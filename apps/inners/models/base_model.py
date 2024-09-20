from pydantic import BaseModel as PydanticBaseModelV2, ConfigDict as ConfigDictV2


class BaseModel(PydanticBaseModelV2):
    model_config = ConfigDictV2(
        arbitrary_types_allowed=True,
        revalidate_instances="always",
        validate_default=True,
        validate_return=True,
        validate_assignment=True,
    )

    def patch_from(self, patcher: dict):
        for key, value in patcher.items():
            if not hasattr(self, key):
                raise ValueError(f"Attribute {key} not found in {self.__class__.__name__}.")
            self.__setattr__(key, value)
        return self
