import uuid
from typing import List

from apps.inners.models.daos.account import Account


class AccountFake:

    def __init__(self):
        self._data: List[Account] = [
            Account(
                id=uuid.uuid4(),
                email=f"email{uuid.uuid4()}@mail.com",
                password="password0"
            ),
            Account(
                id=uuid.uuid4(),
                email=f"email{uuid.uuid4()}@mail.com",
                password="password1"
            )
        ]

    @property
    def data(self) -> List[Account]:
        return [Account(**account.dict()) for account in self._data]

    def delete_many_by_id(self, id: uuid.UUID):
        is_found: bool = False
        for account in self._data:
            if account.id == id:
                is_found = True
                self._data.remove(account)

        if not is_found:
            raise ValueError(f"Account with id {id} is not found.")
