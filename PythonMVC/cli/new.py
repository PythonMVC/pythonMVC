"""`pmvc new` command implementation."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import typer

from ._utils import write_files
from .scaffold_templates import (
    ALEMBIC_ENV,
    ALEMBIC_INI,
    POSTS_CONTROLLER,
    POSTS_MODEL,
    POSTS_SCHEMAS,
    POSTS_VIEWS,
    PROJECT_SKELETON,
    PYPROJECT,
)


DATABASE_URLS: Dict[str, tuple[str, str]] = {
    "sqlite": ("sqlite:///db/app.db", "# using SQLite dev database"),
    "mysql": ("mysql+pymysql://user:pass@localhost:3306/{name}", "# requires: pymysql"),
    "postgresql": ("postgresql+psycopg://user:pass@localhost:5432/{name}", "# requires: psycopg[binary]"),
}


def _specialize_main_py(content: str, database: str, project_name: str) -> str:
    url, hint = DATABASE_URLS[database]
    url = url.format(name=project_name)
    marker = "DATABASE_URL = 'sqlite:///db/app.db'  # swap to postgresql+psycopg://, mysql+pymysql://, or mongodb://"
    replacement = f"DATABASE_URL = '{url}'  {hint}"
    return content.replace(marker, replacement)


def _write_project_skeleton(root: Path, database: str) -> None:
    files = dict(PROJECT_SKELETON)
    files["app/main.py"] = _specialize_main_py(PROJECT_SKELETON["app/main.py"], database, root.name)
    write_files(root, files)


def _write_resource_examples(root: Path) -> None:
    write_files(
        root,
        {
            "app/controllers/posts_controller.py": POSTS_CONTROLLER,
            "app/models/post.py": POSTS_MODEL,
            "app/controllers/schemas.py": POSTS_SCHEMAS,
        },
    )
    write_files(root, POSTS_VIEWS)


def _write_alembic_scaffolding(root: Path) -> None:
    (root / "alembic").mkdir(parents=True, exist_ok=True)
    (root / "alembic" / "env.py").write_text(ALEMBIC_ENV)
    (root / "alembic.ini").write_text(ALEMBIC_INI)


def new(name: str, database: str = "sqlite") -> None:
    """Create a new PythonMVC project with an example Posts resource."""
    db = database.lower()
    if db not in DATABASE_URLS:
        raise typer.BadParameter("database must be one of: sqlite, mysql, postgresql")

    root = Path(name)
    (root / "PythonMVC").mkdir(parents=True, exist_ok=True)

    (root / "pyproject.toml").write_text(PYPROJECT)
    _write_project_skeleton(root, db)
    _write_resource_examples(root)
    _write_alembic_scaffolding(root)

    typer.echo(f"✔ Created project at {root.resolve()}")
    typer.echo(
        "Next steps:\n"
        f"  cd {name}\n"
        "  pip install -e .\n"
        '  pmvc db init && pmvc db migrate "init" && pmvc db upgrade && pmvc server'
    )
