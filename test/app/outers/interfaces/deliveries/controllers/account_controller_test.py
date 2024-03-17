import json
import uuid

import bcrypt
import pytest as pytest
import pytest_asyncio
from httpx import Response

from app.inners.models.daos.account import Account
from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.managements.accounts.create_one_body import \
    CreateOneBody
from app.inners.models.dtos.contracts.requests.managements.accounts.patch_one_body import \
    PatchOneBody
from test.containers.test_container import TestContainer
from test.main import MainTest

url_path: str = "/api/accounts"


@pytest_asyncio.fixture(scope="function", autouse=True)
async def run_around(request: pytest.FixtureRequest):
    test_container: TestContainer = TestContainer()
    main_test = MainTest(
        all_seeder=test_container.seeders.all_seeder()
    )
    await main_test.all_seeder.up()
    yield main_test
    await main_test.all_seeder.down()


@pytest.mark.asyncio
async def test__find_one_by_id__should_return_one_account__succeed(run_around: MainTest):
    selected_account_mock: Account = run_around.all_seeder.account_seeder.account_mock.data[0]
    response: Response = await run_around.client.get(
        url=f"{url_path}/{selected_account_mock.id}"
    )
    assert response.status_code == 200
    response_body: Content[Account] = Content[Account](**response.json())
    assert response_body.data == selected_account_mock


@pytest.mark.asyncio
async def test__create_one__should_create_one_account__succeed(run_around: MainTest):
    account_to_create_body: CreateOneBody = CreateOneBody(
        email=f"email{uuid.uuid4()}@mail.com",
        password="password0",
    )
    response: Response = await run_around.client.post(
        url=url_path,
        json=json.loads(account_to_create_body.json())
    )
    assert response.status_code == 201
    response_body: Content[Account] = Content[Account](**response.json())
    assert response_body.data.email == account_to_create_body.email
    assert bcrypt.checkpw(account_to_create_body.password.encode(), response_body.data.password.encode()) is True


@pytest.mark.asyncio
async def test__patch_one_by_id__should_patch_one_account__succeed(run_around: MainTest):
    selected_account_mock: Account = run_around.all_seeder.account_seeder.account_mock.data[0]
    account_to_patch_body: PatchOneBody = PatchOneBody(
        email=f"patched.email{uuid.uuid4()}@mail.com",
        password="patched.password1",
    )
    response: Response = await run_around.client.patch(
        url=f"{url_path}/{selected_account_mock.id}",
        json=json.loads(account_to_patch_body.json())
    )
    assert response.status_code == 200
    response_body: Content[Account] = Content[Account](**response.json())
    assert response_body.data.email == account_to_patch_body.email
    assert bcrypt.checkpw(account_to_patch_body.password.encode(), response_body.data.password.encode()) is True


@pytest.mark.asyncio
async def test__delete_one_by_id__should_delete_one_account__succeed(run_around: MainTest):
    selected_account_mock: Account = run_around.all_seeder.account_seeder.account_mock.data[0]
    response: Response = await run_around.client.delete(
        url=f"{url_path}/{selected_account_mock.id}"
    )
    assert response.status_code == 200
    response_body: Content[Account] = Content[Account](**response.json())
    assert response_body.data == selected_account_mock
    run_around.all_seeder.delete_account_by_id_cascade(selected_account_mock.id)
