import json
import uuid

import bcrypt
import pytest as pytest
from httpx import Response
from starlette import status

from apps.inners.models.daos.account import Account
from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.managements.accounts.create_one_body import \
    CreateOneBody
from apps.inners.models.dtos.contracts.requests.managements.accounts.patch_one_body import \
    PatchOneBody
from tests.main_context import MainContext

url_path: str = "/api/accounts"


@pytest.mark.asyncio
async def test__find_one_by_id__should__succeed(main_context: MainContext):
    selected_account_fake: Account = main_context.all_seeder.account_seeder.account_fake.data[0]
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.get(
        url=f"{url_path}/{selected_account_fake.id}",
        headers=headers
    )
    content: Content[Account] = Content[Account](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.id == selected_account_fake.id
    assert content.data.email == selected_account_fake.email
    assert bcrypt.checkpw(selected_account_fake.password.encode(), content.data.password.encode())


@pytest.mark.asyncio
async def test__create_one__should_create_one_account__succeed(main_context: MainContext):
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    account_creator_body: CreateOneBody = CreateOneBody(
        email=f"email{uuid.uuid4()}@mail.com",
        password="password0",
    )
    headers: dict = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.post(
        url=url_path,
        json=json.loads(account_creator_body.json()),
        headers=headers
    )

    content: Content[Account] = Content[Account](
        **response.json(),
        status_code=response.status_code
    )
    assert content.data.email == account_creator_body.email
    assert bcrypt.checkpw(account_creator_body.password.encode(), content.data.password.encode())


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_account__succeed(main_context: MainContext):
    selected_account_fake: Account = main_context.all_seeder.account_seeder.account_fake.data[0]
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    account_patcher_body: PatchOneBody = PatchOneBody(
        email=f"patched.email{uuid.uuid4()}@mail.com",
        password="patched.password1",
    )
    headers: dict = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.patch(
        url=f"{url_path}/{selected_account_fake.id}",
        json=json.loads(account_patcher_body.json()),
        headers=headers
    )

    content: Content[Account] = Content[Account](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.email == account_patcher_body.email
    assert bcrypt.checkpw(account_patcher_body.password.encode(), content.data.password.encode())


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_account__succeed(main_context: MainContext):
    selected_account_fake: Account = main_context.all_seeder.account_seeder.account_fake.data[0]
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.delete(
        url=f"{url_path}/{selected_account_fake.id}",
        headers=headers
    )

    content: Content[Account] = Content[Account](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.id == selected_account_fake.id
    assert content.data.email == selected_account_fake.email
    assert bcrypt.checkpw(selected_account_fake.password.encode(), content.data.password.encode())
    main_context.all_seeder.delete_many_account_by_id_cascade(selected_account_fake.id)
