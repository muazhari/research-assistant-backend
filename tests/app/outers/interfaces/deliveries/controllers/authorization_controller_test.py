import json

import pytest as pytest
from httpx import Response
from starlette import status

from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.authorizations.refresh_access_token_body import RefreshAccessTokenBody
from tests.main_context import MainContext

url_path: str = "/api/authorizations"


@pytest.mark.asyncio
async def test__refresh_access_token__success(main_context: MainContext) -> None:
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    refresh_access_token_body: RefreshAccessTokenBody = RefreshAccessTokenBody(
        refresh_token=selected_session_fake.refresh_token
    )
    headers: dict = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    params: dict = {
        "type": "access_token"
    }
    response: Response = await main_context.client.post(
        url=f"{url_path}/refreshes",
        json=json.loads(refresh_access_token_body.json()),
        params=params,
        headers=headers
    )

    content: Content[Session] = Content[Session](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.id == selected_session_fake.id
    assert content.data.account_id == selected_session_fake.account_id
    assert content.data.access_token != selected_session_fake.access_token
    assert content.data.refresh_token == selected_session_fake.refresh_token
    assert content.data.access_token_expired_at > selected_session_fake.access_token_expired_at
    assert content.data.refresh_token_expired_at == selected_session_fake.refresh_token_expired_at
