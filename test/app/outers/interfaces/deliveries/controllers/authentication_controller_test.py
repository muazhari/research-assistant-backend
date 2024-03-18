import json
import uuid
from typing import Any

import bcrypt
import pytest as pytest
from httpx import Response

from app.inners.models.daos.account import Account
from app.inners.models.daos.session import Session
from app.inners.models.dtos.contracts.content import Content
from app.inners.models.dtos.contracts.requests.authentications.logins.login_by_email_and_password_body import \
    LoginByEmailAndPasswordBody
from app.inners.models.dtos.contracts.requests.authentications.registers.register_by_email_and_password_body import \
    RegisterByEmailAndPasswordBody
from app.inners.models.dtos.contracts.responses.authentications.logins.login_response import LoginResponse
from app.inners.models.dtos.contracts.responses.authentications.registers.register_response import RegisterResponse
from test.conftest import MainTest

url_path: str = "/api/authentications"


@pytest.mark.asyncio
async def test__login_by_email_and_password__succeed(main_test: MainTest):
    selected_account_mock: Account = main_test.all_seeder.account_seeder.account_mock.data[0]
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    login_by_email_and_password_body: LoginByEmailAndPasswordBody = LoginByEmailAndPasswordBody(
        email=selected_account_mock.email,
        password=selected_account_mock.password
    )
    params: dict = {
        "method": "email_and_password"
    }
    response: Response = await main_test.client.post(
        url=f"{url_path}/logins",
        params=params,
        json=json.loads(login_by_email_and_password_body.json())
    )
    assert response.status_code == 200
    response_body: Content[LoginResponse] = Content[LoginResponse](**response.json())
    assert response_body.data.account.id == selected_account_mock.id
    assert response_body.data.account.email == selected_account_mock.email
    assert bcrypt.checkpw(selected_account_mock.password.encode(), response_body.data.account.password.encode())
    assert response_body.data.session == selected_session_mock


@pytest.mark.asyncio
async def test__login_by_email_and_password__failed__when__email_is_not_found(main_test: MainTest):
    selected_account_mock: Account = main_test.all_seeder.account_seeder.account_mock.data[0]
    login_by_email_and_password_body: LoginByEmailAndPasswordBody = LoginByEmailAndPasswordBody(
        email=f"email{uuid.uuid4()}@mail.com",
        password=selected_account_mock.password,
    )
    params: dict = {
        "method": "email_and_password"
    }
    response: Response = await main_test.client.post(
        url=f"{url_path}/logins",
        params=params,
        json=json.loads(login_by_email_and_password_body.json())
    )
    assert response.status_code == 404
    response_body: Content[LoginResponse] = Content[LoginResponse](**response.json())
    assert response_body.data is None


@pytest.mark.asyncio
async def test__login_by_email_and_password__failed__when__password_is_not_matched(main_test: MainTest):
    selected_account_mock: Account = main_test.all_seeder.account_seeder.account_mock.data[0]
    login_by_email_and_password_body: LoginByEmailAndPasswordBody = LoginByEmailAndPasswordBody(
        email=selected_account_mock.email,
        password=f"password{uuid.uuid4()}"
    )
    params: dict = {
        "method": "email_and_password"
    }
    response: Response = await main_test.client.post(
        url=f"{url_path}/logins",
        params=params,
        json=json.loads(login_by_email_and_password_body.json())
    )
    assert response.status_code == 401
    response_body: Content[LoginResponse] = Content[LoginResponse](**response.json())
    assert response_body.data is None


@pytest.mark.asyncio
async def test__login_by_email_and_password__failed__when__method_is_not_supported(main_test: MainTest):
    selected_account_mock: Account = main_test.all_seeder.account_seeder.account_mock.data[0]
    login_by_email_and_password_body: LoginByEmailAndPasswordBody = LoginByEmailAndPasswordBody(
        email=selected_account_mock.email,
        password=selected_account_mock.password
    )
    params: dict = {
        "method": f"{uuid.uuid4()}"
    }
    response: Response = await main_test.client.post(
        url=f"{url_path}/logins",
        params=params,
        json=json.loads(login_by_email_and_password_body.json())
    )
    assert response.status_code == 400
    response_body: Content[LoginResponse] = Content[LoginResponse](**response.json())
    assert response_body.data is None


@pytest.mark.asyncio
async def test__register_by_email_and_password__succeed(main_test: MainTest):
    register_by_email_and_password_body: RegisterByEmailAndPasswordBody = RegisterByEmailAndPasswordBody(
        email=f"email{uuid.uuid4()}@mail.com",
        password="password0",
    )
    params: dict = {
        "method": "email_and_password"
    }
    response: Response = await main_test.client.post(
        url=f"{url_path}/registers",
        params=params,
        json=json.loads(register_by_email_and_password_body.json())
    )
    assert response.status_code == 201
    response_body: Content[RegisterResponse] = Content[RegisterResponse](**response.json())
    assert response_body.data.account.email == register_by_email_and_password_body.email
    assert bcrypt.checkpw(register_by_email_and_password_body.password.encode(),
                          response_body.data.account.password.encode())


@pytest.mark.asyncio
async def test__register_by_email_and_password__failed__when__method_is_not_supported(main_test: MainTest):
    register_by_email_and_password_body: RegisterByEmailAndPasswordBody = RegisterByEmailAndPasswordBody(
        email=f"email{uuid.uuid4()}@mail.com",
        password="password0",
    )
    params: dict = {
        "method": f"{uuid.uuid4()}"
    }
    response: Response = await main_test.client.post(
        url=f"{url_path}/registers",
        params=params,
        json=json.loads(register_by_email_and_password_body.json())
    )
    assert response.status_code == 400
    response_body: Content[RegisterResponse] = Content[RegisterResponse](**response.json())
    assert response_body.data is None


@pytest.mark.asyncio
async def test__logout__succeed(main_test: MainTest):
    selected_session_mock: Session = main_test.all_seeder.session_seeder.session_mock.data[0]
    headers: dict = {
        "Authorization": f"Bearer {selected_session_mock.access_token}"
    }
    response: Response = await main_test.client.post(
        url=f"{url_path}/logouts",
        headers=headers,
    )
    assert response.status_code == 200
    response_body: Content[Any] = Content[Any](**response.json())
    assert response_body.data is None
    main_test.all_seeder.delete_many_session_by_id_cascade(selected_session_mock.id)
