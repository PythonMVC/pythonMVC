"""PythonMVC CLI entrypoint."""

from __future__ import annotations

import typer

from .database import db as db_command
from .generate import generate as generate_command
from .new import new as new_command

app = typer.Typer(help="PythonMVC CLI — generators and dev tasks")


@app.command("new")
def new(
    name: str = typer.Argument(..., help="App folder name"),
    database: str = typer.Option("sqlite", help="Database backend", case_sensitive=False),
):
    new_command(name, database)


@app.command("server")
def server(host: str = "127.0.0.1", port: int = 8000, reload: bool = True):
    """Run the development server (Uvicorn)."""
    import subprocess

    command = ["uvicorn", "app.main:app", "--host", host, "--port", str(port)]
    if reload:
        command.append("--reload")
    subprocess.run(command, check=False)


@app.command("db")
def db(cmd: str = typer.Argument(..., help="init|migrate|upgrade|downgrade|revision"), message: str = ""):
    db_command(cmd, message)


@app.command("generate")
def generate(
    kind: str,
    name: str,
    fields: list[str] = typer.Argument((), help="Field declarations e.g. title:str body:text"),
):
    joined = " ".join(fields)
    generate_command(kind, name, joined)


def main() -> None:  # pragma: no cover - console entrypoint
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
