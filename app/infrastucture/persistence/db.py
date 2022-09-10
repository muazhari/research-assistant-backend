from sqlalchemy.orm import declarative_base
from sqlmodel import create_engine, Session

from app.infrastucture.config.database_config import database_config

engine = create_engine(database_config.DATABASE_URL)

session = Session(engine)

Base = declarative_base()

metadata = Base.metadata
