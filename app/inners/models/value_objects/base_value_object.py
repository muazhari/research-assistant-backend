from pydantic import BaseModel


class BaseValueObject(BaseModel):
    def patch_from(self, entity: dict):
        for key, value in entity.items():
            if not hasattr(self, key):
                raise AttributeError(f"Attribute {key} does not exist.")
            self.__setattr__(key, value)
        return self
