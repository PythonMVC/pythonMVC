"""`pymvc db` command implementation."""

from __future__ import annotations

import subprocess
from pathlib import Path

import typer


def _run(command: list[str]) -> None:
    subprocess.run(command, check=False)


def db(cmd: str, message: str = "") -> None:
    """Database tasks proxied to Alembic with sane defaults."""
    if cmd == "init":
        Path("db").mkdir(exist_ok=True, parents=True)
        typer.echo("✔ DB directory ensured at ./db")
        return

    if cmd == "migrate":
        _run(["alembic", "revision", "--autogenerate", "-m", message or "change"])
        return

    if cmd == "upgrade":
        _run(["alembic", "upgrade", "head"])
        return

    if cmd == "downgrade":
        _run(["alembic", "downgrade", "-1"])
        return

    if cmd == "revision":
        _run(["alembic", "revision", "-m", message or "manual"])
        return

    typer.echo("Unknown db command")

