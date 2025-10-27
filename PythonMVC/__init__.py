"""PythonMVC — Rails-inspired conventions on top of Starlette + SQLAlchemy."""

from .app import create_app
from .router import resource
from .model import BaseModel, db_session

# SPDX-License-Identifier: Apache-2.0
__version__ = "0.0.1"

__all__ = [
    "create_app",
    "resource",
    "BaseModel",
    "db_session",
]

