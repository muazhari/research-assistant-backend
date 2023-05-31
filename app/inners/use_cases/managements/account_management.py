import uuid
from typing import List

from app.inners.models.entities.account import Account
from app.inners.models.value_objects.contracts.requests.managements.accounts.create_one_request import CreateOneRequest
from app.inners.models.value_objects.contracts.requests.managements.accounts.delete_one_by_id_request import \
    DeleteOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.accounts.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.accounts.read_all_request import ReadAllRequest
from app.inners.models.value_objects.contracts.requests.managements.accounts.read_one_by_id_request import \
    ReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.outers.repositories.account_repository import AccountRepository
from app.outers.utilities.management_utility import ManagementUtility


class AccountManagement:
    def __init__(self):
        self.management_utility: ManagementUtility = ManagementUtility()
        self.account_repository: AccountRepository = AccountRepository()

    async def read_all(self, request: ReadAllRequest) -> Content[List[Account]]:
        try:
            found_entities: List[Account] = await self.account_repository.read_all()

            if len(request.query_parameter.keys()) > 0:
                found_entities = list(
                    filter(
                        lambda entity: self.management_utility.filter(request.query_parameter, entity),
                        found_entities
                    )
                )

            content: Content[List[Account]] = Content(
                data=found_entities,
                message="Account read all succeed."
            )
        except Exception as exception:
            content: Content[List[Account]] = Content(
                data=None,
                message=f"Account read all failed: {exception}"
            )
        return content

    async def read_one_by_id(self, request: ReadOneByIdRequest) -> Content[Account]:
        try:
            found_entity: Account = await self.account_repository.read_one_by_id(request.id)
            content: Content[Account] = Content(
                data=found_entity,
                message="Account read one by id succeed."
            )
        except Exception as exception:
            content: Content[Account] = Content(
                data=None,
                message=f"Account read one by id failed: {exception}"
            )
        return content


    async def read_one_by_email(self, email: str) -> Content[Account]:
        try:
            found_entity: Account = await self.account_repository.read_one_by_email(email)
            content: Content[Account] = Content(
                data=found_entity,
                message="Account read one by email succeed."
            )
        except Exception as exception:
            content: Content[Account] = Content(
                data=None,
                message=f"Account read one by email failed: {exception}"
            )
        return content

    async def read_one_by_email_and_password(self, email: str, password: str) -> Content[Account]:
        try:
            found_entity: Account = await self.account_repository.read_one_by_email_and_password(email, password)
            content: Content[Account] = Content(
                data=found_entity,
                message="Account read one by email and password succeed."
            )
        except Exception as exception:
            content: Content[Account] = Content(
                data=None,
                message=f"Account read one by email and password failed: {exception}"
            )
        return content

    async def create_one(self, request: CreateOneRequest) -> Content[Account]:
        try:
            entity_to_create: Account = Account(
                **request.body.dict(),
                id=uuid.uuid4(),
            )
            created_entity: Account = await self.account_repository.create_one(entity_to_create)
            content: Content[Account] = Content(
                data=created_entity,
                message="Account create one succeed."
            )
        except Exception as exception:
            content: Content[Account] = Content(
                data=None,
                message=f"Account create one failed: {exception}"
            )
        return content

    async def patch_one_by_id(self, request: PatchOneByIdRequest) -> Content[Account]:
        try:
            entity_to_patch: Account = Account(
                **request.body.dict(),
                id=request.id,
            )
            patched_entity: Account = await self.account_repository.patch_one_by_id(request.id, entity_to_patch)
            content: Content[Account] = Content(
                data=patched_entity,
                message="Account patch one by id succeed."
            )
        except Exception as exception:
            content: Content[Account] = Content(
                data=None,
                message=f"Account patch one by id failed: {exception}"
            )
        return content

    async def delete_one_by_id(self, request: DeleteOneByIdRequest) -> Content[Account]:
        try:
            deleted_entity: Account = await self.account_repository.delete_one_by_id(request.id)
            content: Content[Account] = Content(
                data=deleted_entity,
                message="Account delete one by id succeed."
            )
        except Exception as exception:
            content: Content[Account] = Content(
                data=None,
                message=f"Account delete one by id failed: {exception}"
            )
        return content
