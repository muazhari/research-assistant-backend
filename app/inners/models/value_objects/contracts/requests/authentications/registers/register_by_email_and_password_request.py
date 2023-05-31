from app.inners.models.value_objects.base_value_object import BaseValueObject

from app.inners.models.value_objects.contracts.requests.authentications.registers.register_by_email_and_password_body import \
    RegisterByEmailAndPasswordBody


class RegisterByEmailAndPasswordRequest(BaseValueObject):
    body: RegisterByEmailAndPasswordBody
