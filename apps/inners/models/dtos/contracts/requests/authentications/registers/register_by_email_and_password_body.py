from apps.inners.models.dtos.base_dto import BaseDto


class RegisterByEmailAndPasswordBody(BaseDto):
    email: str
    password: str
