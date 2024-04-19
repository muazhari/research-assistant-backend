from apps.inners.models.daos.account import Account
from apps.inners.models.dtos.base_dto import BaseDto


class RegisterResponse(BaseDto):
    account: Account
