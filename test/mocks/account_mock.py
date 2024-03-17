import uuid
from typing import List

import bcrypt

from app.inners.models.daos.account import Account


class AccountMock:

    def __init__(self):
        self._data: List[Account] = [
            Account(
                id=uuid.uuid4(),
                email=f"email{uuid.uuid4()}@mail.com",
                password=bcrypt.hashpw("password0".encode(), bcrypt.gensalt()).decode(),
            ),
            Account(
                id=uuid.uuid4(),
                email=f"email{uuid.uuid4()}@mail.com",
                password=bcrypt.hashpw("password1".encode(), bcrypt.gensalt()).decode(),
            )
        ]

    @property
    def data(self) -> List[Account]:
        return [Account(**account.dict()) for account in self._data]

    def delete_by_id(self, id: uuid.UUID):
        is_found: bool = False
        for account in self._data:
            if account.id == id:
                is_found = True
                self._data.remove(account)

        if not is_found:
            raise ValueError(f"Account with id {id} is not found.")
