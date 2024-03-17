from sqlmodel import SQLModel


class BaseDao(SQLModel):
    def patch_from(self, dao: dict):
        for key, value in dao.items():
            if not hasattr(self, key):
                raise AttributeError(f"Attribute {key} is not exist.")
            self.__setattr__(key, value)
        return self