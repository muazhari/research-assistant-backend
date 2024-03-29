import uuid
from typing import List

from app.inners.models.entities.account import Account


class AccountMockData:

    def __init__(self):
        self.data: List[Account] = [
            Account(
                id=uuid.uuid4(),
                name="name0",
                email="email0",
                password="password0",
            ),
            Account(
                id=uuid.uuid4(),
                name="name1",
                email="email1",
                password="password1",
            )
        ]
