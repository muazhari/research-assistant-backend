import json

import pytest as pytest
from httpx import Response

from app.inners.models.daos.session import Session
from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.authorizations.refresh_access_token_body import RefreshAccessTokenBody
from test.conftest import MainTest

url_path: str = "/api/authorizations"


@pytest.mark.asyncio
async def test__refresh_access_token__success(main_test: MainTest) -> None:
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    refresh_access_token_body: RefreshAccessTokenBody = RefreshAccessTokenBody(
        refresh_token=selected_session_mock.refresh_token
    )
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    params: dict = {
        "type": "access_token"
    }
    response: Response = await main_test.client.post(
        url=f"{url_path}/refreshes",
        json=json.loads(refresh_access_token_body.json()),
        params=params,
        headers=headers
    )
    assert response.status_code == 200
    response_body: Content[Session] = Content[Session](**response.json())
    assert response_body.data.id == selected_session_mock.id
    assert response_body.data.account_id == selected_session_mock.account_id
    assert response_body.data.access_token != selected_session_mock.access_token
    assert response_body.data.refresh_token == selected_session_mock.refresh_token
    assert response_body.data.access_token_expired_at > selected_session_mock.access_token_expired_at
    assert response_body.data.refresh_token_expired_at == selected_session_mock.refresh_token_expired_at
