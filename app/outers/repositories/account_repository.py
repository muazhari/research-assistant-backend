from typing import List
from uuid import UUID

from sqlmodel import select
from sqlmodel.sql import expression

from app.inners.models.entities.account import Account
from app.outers.persistences.datastore_one_persistence import DataStorePersistence


class AccountRepository:

    def __init__(self):
        self.datastore_persistence: DataStorePersistence = DataStorePersistence()

    async def read_all(self) -> List[Account]:
        async with await self.datastore_persistence.create_session() as session:
            statement: expression = select(Account)
            result = await session.execute(statement)
            found_entities: List[Account] = result.scalars().all()
            return found_entities

    async def read_one_by_id(self, id: UUID) -> Account:
        async with await self.datastore_persistence.create_session() as session:
            statement: expression = select(Account).where(Account.id == id)
            result = await session.execute(statement)
            found_entity: Account = result.scalars().one()
            if found_entity is None:
                raise Exception("Entity not found.")
            return found_entity

    async def read_one_by_email_and_password(self, email: str, password: str) -> Account:
        async with await self.datastore_persistence.create_session() as session:
            statement: expression = select(Account).where(Account.email == email).where(
                Account.password == password)
            result = await session.execute(statement)
            found_entity: Account = result.scalars().one()
            if found_entity is None:
                raise Exception("Entity not found.")
            return found_entity

    async def read_one_by_email(self, email: str) -> Account:
        async with await self.datastore_persistence.create_session() as session:
            statement: expression = select(Account).where(Account.email == email)
            result = await session.execute(statement)
            found_entity: Account = result.scalars().one()
            if found_entity is None:
                raise Exception("Entity not found.")
            return found_entity

    async def create_one(self, entity: Account) -> Account:
        async with await self.datastore_persistence.create_session() as session:
            try:
                session.add(entity)
                await session.commit()
                await session.refresh(entity)
            except Exception as exception:
                raise exception
        return entity

    async def patch_one_by_id(self, id: UUID, entity: Account) -> Account:
        async with await self.datastore_persistence.create_session() as session:
            try:
                statement: expression = select(Account).where(Account.id == id)
                result = await session.execute(statement)
                found_entity: Account = result.scalars().one()
                if found_entity is None:
                    raise Exception("Entity not found.")
                found_entity.patch_from(entity.dict())
                await session.commit()
                await session.refresh(found_entity)
            except Exception as exception:
                raise exception
            return found_entity

    async def delete_one_by_id(self, id: UUID) -> Account:
        async with await self.datastore_persistence.create_session() as session:
            try:
                statement: expression = select(Account).where(Account.id == id)
                result = await session.execute(statement)
                found_entity: Account = result.scalars().one()
                if found_entity is None:
                    raise Exception("Entity not found.")
                await session.delete(found_entity)
                await session.commit()
            except Exception as exception:
                raise exception
            return found_entity
