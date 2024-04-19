from apps.inners.models.daos.account import Account
from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.base_dto import BaseDto


class LoginResponse(BaseDto):
    account: Account
    session: Session
