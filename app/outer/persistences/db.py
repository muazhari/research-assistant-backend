from sqlalchemy.orm import declarative_base
from sqlmodel import create_engine, Session

from app.outer.settings.database_settings import database_settings

engine = create_engine(database_settings.DATABASE_URL)


def create_session():
    return Session(engine)
