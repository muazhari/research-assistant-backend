from app.inners.models.value_objects.base_value_object import BaseValueObject


class LoginByEmailAndPasswordBody(BaseValueObject):
    email: str
    password: str
