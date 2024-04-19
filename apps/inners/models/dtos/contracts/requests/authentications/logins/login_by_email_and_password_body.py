from apps.inners.models.dtos.base_dto import BaseDto


class LoginByEmailAndPasswordBody(BaseDto):
    email: str
    password: str
