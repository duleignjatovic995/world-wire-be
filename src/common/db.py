from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from src.settings import settings

engine = create_engine(
    settings.DB_CONNECTION,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

Base = declarative_base(metadata=meta)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
