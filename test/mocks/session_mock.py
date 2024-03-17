import uuid
from datetime import datetime, timedelta, timezone
from typing import List

from app.inners.models.daos.session import Session
from test.mocks.account_mock import AccountMock


class SessionMock:

    def __init__(
            self,
            account_mock: AccountMock
    ):
        self.account_mock: AccountMock = account_mock
        current_time: datetime = datetime.now(tz=timezone.utc)
        self._data: List[Session] = [
            Session(
                id=uuid.uuid4(),
                account_id=self.account_mock.data[0].id,
                access_token=uuid.uuid4(),
                refresh_token=uuid.uuid4(),
                access_token_expired_at=current_time + timedelta(minutes=10),
                refresh_token_expired_at=current_time + timedelta(days=15),
            ),
            Session(
                id=uuid.uuid4(),
                account_id=self.account_mock.data[1].id,
                access_token=uuid.uuid4(),
                refresh_token=uuid.uuid4(),
                access_token_expired_at=current_time + timedelta(minutes=10),
                refresh_token_expired_at=current_time + timedelta(days=15),
            )
        ]

    @property
    def data(self) -> List[Session]:
        return [Session(**session.dict()) for session in self._data]

    def delete_by_id(self, id: uuid.UUID):
        is_found: bool = False
        for session in self._data:
            if session.id == id:
                is_found = True
                self._data.remove(session)

        if not is_found:
            raise ValueError(f"Session with id {id} is not found.")
