"""ORM helpers built on SQLAlchemy."""

from __future__ import annotations

import os
from typing import Optional

from sqlalchemy import DateTime, create_engine, func
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

_engine: Engine | None = None
_SessionFactory: sessionmaker[Session] | None = None


class Base(DeclarativeBase):
    """Declarative base so projects can extend shared metadata."""


class BaseModel(Base):
    """Common columns and helpers for ActiveRecord-style models."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    @classmethod
    def engine(cls) -> Engine:
        global _engine
        if _engine is None:
            url = os.getenv("DATABASE_URL", "sqlite:///db/app.db")
            _engine = create_engine(url, echo=False, future=True)
        return _engine

    @classmethod
    def create_all(cls) -> None:
        cls.metadata.create_all(cls.engine())


def db_session() -> Session:
    """Return a new SQLAlchemy Session bound to the configured engine."""
    global _SessionFactory
    if _SessionFactory is None:
        _SessionFactory = sessionmaker(bind=BaseModel.engine(), class_=Session, expire_on_commit=False)
    return _SessionFactory()

