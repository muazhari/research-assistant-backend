import datetime
import uuid
from typing import List
from uuid import UUID

from app.inner.model.entities.account import Account
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.account.create_one_request import \
    CreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.account.patch_one_by_id_request import \
    PatchOneByIdRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content
from app.outer.repositories.account_repository import account_repository


class AccountManager:
    def read_all(self) -> Content[List[Account]]:
        data: Account = account_repository.read_all()
        content: Content[List[Account]] = Content[List[Account]](
            message="Read all account succeed.",
            data=data
        )
        return content

    def read_one_by_id(self, id: UUID) -> Content[Account]:
        data: Account = account_repository.read_one_by_id(id)
        content: Content[Account] = Content[Account](
            message="Read one account succeed.",
            data=data
        )
        return content

    def create_one(self, entity_request: CreateOneRequest) -> Content[Account]:
        entity: Account = Account(
            id=uuid.uuid4(),
            name=entity_request.name,
            email=entity_request.email,
            password=entity_request.password,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )

        data: Account = account_repository.create_one(entity)
        content: Content[Account] = Content[Account](
            message="Create one account succeed.",
            data=data
        )
        return content

    def patch_one_by_id(self, id: UUID, entity_request: PatchOneByIdRequest) -> Content[Account]:
        found_entity: Account = account_repository.read_one_by_id(id)

        entity: Account = Account(
            id=found_entity.id,
            name=entity_request.name,
            email=entity_request.email,
            password=entity_request.password,
            created_at=found_entity.created_at,
            updated_at=datetime.datetime.now()
        )

        data: Account = account_repository.patch_one_by_id(id, entity)
        content: Content[Account] = Content[Account](
            message="Patch one account succeed.",
            data=data
        )
        return content

    def delete_one_by_id(self, id: UUID) -> Content[Account]:
        data: Account = account_repository.delete_one_by_id(id)
        content: Content[Account] = Content[Account](
            message="Delete one account succeed.",
            data=data
        )
        return content


account_manager = AccountManager()
