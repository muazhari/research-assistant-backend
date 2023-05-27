import uuid

from app.inners.models.entities.account import Account


class AccountMockData:
    def get_data(self) -> dict:
        return {
            "account": [
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
        }
