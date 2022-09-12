import pydash
from pydantic import BaseModel


class BaseEntity(BaseModel):
    class Config:
        alias_generator = pydash.camel_case
        allow_population_by_field_name = True
