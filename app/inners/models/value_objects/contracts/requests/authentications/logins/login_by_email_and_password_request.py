from app.inners.models.value_objects.base_value_object import BaseValueObject
from app.inners.models.value_objects.contracts.requests.authentications.logins.login_by_email_and_password_body import \
    LoginByEmailAndPasswordBody


class LoginByEmailAndPasswordRequest(BaseValueObject):
    body: LoginByEmailAndPasswordBody
