from app.inners.models.daos.account import Account
from app.inners.models.dtos.base_dto import BaseDto


class RegisterResponse(BaseDto):
    account: Account
