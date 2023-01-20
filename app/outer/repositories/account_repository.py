from uuid import UUID

from sqlmodel import select
from sqlmodel.sql import expression

from app.inner.model.entities.account import Account
from app.outer.persistences.db import create_session


class AccountRepository:

    def read_all(self) -> [Account]:
        with create_session() as session:
            statement: expression = select(Account)
            return session.exec(statement).all()

    def read_one_by_id(self, id: UUID) -> Account:
        with create_session() as session:
            statement: expression = select(Account).where(Account.id == id)
            found_entity: Account = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            return found_entity

    def create_one(self, entity: Account) -> Account:
        with create_session() as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def patch_one_by_id(self, id: UUID, entity: Account) -> Account:
        with create_session() as session:
            statement: expression = select(Account).where(Account.id == id)
            found_entity: Account = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            found_entity.id = entity.id
            found_entity.name = entity.name
            found_entity.email = entity.email
            found_entity.password = entity.password
            found_entity.updated_at = entity.updated_at
            found_entity.created_at = entity.created_at
            session.commit()
            session.refresh(found_entity)
            return found_entity

    def delete_one_by_id(self, id: UUID) -> Account:
        with create_session() as session:
            statement: expression = select(Account).where(Account.id == id)
            found_entity: Account = session.exec(statement).first()
            if found_entity is None:
                raise Exception('Entity not found.')
            session.delete(found_entity)
            session.commit()
            return found_entity


account_repository = AccountRepository()
