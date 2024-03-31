import json
import uuid
from typing import Any

import bcrypt
import pytest as pytest
from httpx import Response
from starlette import status

from apps.inners.models.daos.account import Account
from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.authentications.logins.login_by_email_and_password_body import \
    LoginByEmailAndPasswordBody
from apps.inners.models.dtos.contracts.requests.authentications.registers.register_by_email_and_password_body import \
    RegisterByEmailAndPasswordBody
from apps.inners.models.dtos.contracts.responses.authentications.logins.login_response import LoginResponse
from apps.inners.models.dtos.contracts.responses.authentications.registers.register_response import RegisterResponse
from tests.main_context import MainContext

url_path: str = "/api/authentications"


@pytest.mark.asyncio
async def test__login_by_email_and_password__succeed(main_context: MainContext):
    selected_account_mock: Account = main_context.all_seeder.account_seeder.account_mock.data[0]
    selected_session_mock: Session = main_context.all_seeder.session_seeder.session_mock.data[0]
    login_by_email_and_password_body: LoginByEmailAndPasswordBody = LoginByEmailAndPasswordBody(
        email=selected_account_mock.email,
        password=selected_account_mock.password
    )
    params: dict = {
        "method": "email_and_password"
    }
    response: Response = await main_context.client.post(
        url=f"{url_path}/logins",
        params=params,
        json=json.loads(login_by_email_and_password_body.json())
    )

    content: Content[LoginResponse] = Content[LoginResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data.account.id == selected_account_mock.id
    assert content.data.account.email == selected_account_mock.email
    assert bcrypt.checkpw(selected_account_mock.password.encode(), content.data.account.password.encode())
    assert content.data.session == selected_session_mock


@pytest.mark.asyncio
async def test__login_by_email_and_password__failed__when__email_is_not_found(main_context: MainContext):
    selected_account_mock: Account = main_context.all_seeder.account_seeder.account_mock.data[0]
    login_by_email_and_password_body: LoginByEmailAndPasswordBody = LoginByEmailAndPasswordBody(
        email=f"email{uuid.uuid4()}@mail.com",
        password=selected_account_mock.password,
    )
    params: dict = {
        "method": "email_and_password"
    }
    response: Response = await main_context.client.post(
        url=f"{url_path}/logins",
        params=params,
        json=json.loads(login_by_email_and_password_body.json())
    )

    content: Content[LoginResponse] = Content[LoginResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_404_NOT_FOUND
    assert content.data is None


@pytest.mark.asyncio
async def test__login_by_email_and_password__failed__when__password_is_not_matched(main_context: MainContext):
    selected_account_mock: Account = main_context.all_seeder.account_seeder.account_mock.data[0]
    login_by_email_and_password_body: LoginByEmailAndPasswordBody = LoginByEmailAndPasswordBody(
        email=selected_account_mock.email,
        password=f"password{uuid.uuid4()}"
    )
    params: dict = {
        "method": "email_and_password"
    }
    response: Response = await main_context.client.post(
        url=f"{url_path}/logins",
        params=params,
        json=json.loads(login_by_email_and_password_body.json())
    )

    content: Content[LoginResponse] = Content[LoginResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_401_UNAUTHORIZED
    assert content.data is None


@pytest.mark.asyncio
async def test__login_by_email_and_password__failed__when__method_is_not_supported(main_context: MainContext):
    selected_account_mock: Account = main_context.all_seeder.account_seeder.account_mock.data[0]
    login_by_email_and_password_body: LoginByEmailAndPasswordBody = LoginByEmailAndPasswordBody(
        email=selected_account_mock.email,
        password=selected_account_mock.password
    )
    params: dict = {
        "method": f"{uuid.uuid4()}"
    }
    response: Response = await main_context.client.post(
        url=f"{url_path}/logins",
        params=params,
        json=json.loads(login_by_email_and_password_body.json())
    )

    content: Content[LoginResponse] = Content[LoginResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_400_BAD_REQUEST
    assert content.data is None


@pytest.mark.asyncio
async def test__register_by_email_and_password__succeed(main_context: MainContext):
    register_by_email_and_password_body: RegisterByEmailAndPasswordBody = RegisterByEmailAndPasswordBody(
        email=f"email{uuid.uuid4()}@mail.com",
        password="password0",
    )
    params: dict = {
        "method": "email_and_password"
    }
    response: Response = await main_context.client.post(
        url=f"{url_path}/registers",
        params=params,
        json=json.loads(register_by_email_and_password_body.json())
    )

    content: Content[RegisterResponse] = Content[RegisterResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_201_CREATED
    assert content.data.account.email == register_by_email_and_password_body.email
    assert bcrypt.checkpw(register_by_email_and_password_body.password.encode(),
                          content.data.account.password.encode())


@pytest.mark.asyncio
async def test__register_by_email_and_password__failed__when__method_is_not_supported(main_context: MainContext):
    register_by_email_and_password_body: RegisterByEmailAndPasswordBody = RegisterByEmailAndPasswordBody(
        email=f"email{uuid.uuid4()}@mail.com",
        password="password0",
    )
    params: dict = {
        "method": f"{uuid.uuid4()}"
    }
    response: Response = await main_context.client.post(
        url=f"{url_path}/registers",
        params=params,
        json=json.loads(register_by_email_and_password_body.json())
    )

    content: Content[RegisterResponse] = Content[RegisterResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_400_BAD_REQUEST
    assert content.data is None


@pytest.mark.asyncio
async def test__logout__succeed(main_context: MainContext):
    selected_session_mock: Session = main_context.all_seeder.session_seeder.session_mock.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_context.client.post(
        url=f"{url_path}/logouts",
        headers=headers,
    )

    content: Content[Any] = Content[Any](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert content.data is None
    main_context.all_seeder.delete_many_session_by_id_cascade(selected_session_mock.id)
