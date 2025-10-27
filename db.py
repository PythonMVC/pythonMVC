"""Database adapter helpers."""

from sqlalchemy.orm import Session

from .model import db_session


class Database:
    """Simple façade for obtaining database sessions."""

    def sql(self) -> Session:
        return db_session()

