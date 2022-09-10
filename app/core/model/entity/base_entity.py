from pydantic import BaseModel


def camel_to_snake_case(string: str) -> str:
    return ''.join(['_' + i.lower() if i.isupper() else i for i in string]).lstrip('_')


def snake_to_camel_case(string: str) -> str:
    string_split = string.split('_')
    return string_split[0] + ''.join(word.capitalize() for word in string_split[1:])


class BaseEntity(BaseModel):
    class Config:
        alias_generator = snake_to_camel_case
