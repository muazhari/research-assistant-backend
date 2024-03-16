from app.inners.models.daos.account import Account
from app.inners.models.daos.session import Session
from app.inners.models.dtos.base_dto import BaseDto


class LoginResponse(BaseDto):
    account: Account
    session: Session
