import json
import json
import uuid

import bcrypt
import pytest as pytest
from httpx import Response

from app.inners.models.daos.account import Account
from app.inners.models.daos.session import Session
from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.managements.accounts.create_one_body import \
    CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.accounts.patch_one_body import \
    PatchOneBody
from test.conftest import MainTest

url_path: str = "/api/accounts"


@pytest.mark.asyncio
async def test__find_one_by_id__should__succeed(main_test: MainTest):
    selected_account_mock: Account = main_test.all_seeder.account_seeder.account_mock.data[0]
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.get(
        url=f"{url_path}/{selected_account_mock.id}",
        headers=headers
    )
    assert response.status_code == 200
    response_body: Content[Account] = Content[Account](**response.json())
    assert response_body.data.id == selected_account_mock.id
    assert response_body.data.email == selected_account_mock.email
    assert bcrypt.checkpw(selected_account_mock.password.encode(), response_body.data.password.encode())


@pytest.mark.asyncio
async def test__create_one__should_create_one_account__succeed(main_test: MainTest):
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    account_to_create_body: CreateOneBody = CreateOneBody(
        email=f"email{uuid.uuid4()}@mail.com",
        password="password0",
    )
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.post(
        url=url_path,
        json=json.loads(account_to_create_body.json()),
        headers=headers
    )

    assert response.status_code == 201
    response_body: Content[Account] = Content[Account](**response.json())
    assert response_body.data.email == account_to_create_body.email
    assert bcrypt.checkpw(account_to_create_body.password.encode(), response_body.data.password.encode())


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_account__succeed(main_test: MainTest):
    selected_account_mock: Account = main_test.all_seeder.account_seeder.account_mock.data[0]
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    account_to_patch_body: PatchOneBody = PatchOneBody(
        email=f"patched.email{uuid.uuid4()}@mail.com",
        password="patched.password1",
    )
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.patch(
        url=f"{url_path}/{selected_account_mock.id}",
        json=json.loads(account_to_patch_body.json()),
        headers=headers
    )

    assert response.status_code == 200
    response_body: Content[Account] = Content[Account](**response.json())
    assert response_body.data.email == account_to_patch_body.email
    assert bcrypt.checkpw(account_to_patch_body.password.encode(), response_body.data.password.encode())


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_account__succeed(main_test: MainTest):
    selected_account_mock: Account = main_test.all_seeder.account_seeder.account_mock.data[0]
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.delete(
        url=f"{url_path}/{selected_account_mock.id}",
        headers=headers
    )

    assert response.status_code == 200
    response_body: Content[Account] = Content[Account](**response.json())
    assert response_body.data.id == selected_account_mock.id
    assert response_body.data.email == selected_account_mock.email
    assert bcrypt.checkpw(selected_account_mock.password.encode(), response_body.data.password.encode())
    main_test.all_seeder.delete_many_account_by_id_cascade(selected_account_mock.id)
