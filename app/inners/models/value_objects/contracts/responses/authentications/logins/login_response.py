from app.inners.models.entities.account import Account
from app.inners.models.value_objects.base_value_object import BaseValueObject


class LoginResponse(BaseValueObject):
    account: Account
