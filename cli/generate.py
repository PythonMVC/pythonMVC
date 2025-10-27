"""`pmvc generate` command implementation."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import typer

from ._utils import snake_case

FIELD_SQL_TYPES: Dict[str, str] = {
    "str": "String(255)",
    "text": "Text()",
    "int": "Integer()",
}


def _build_model_columns(fields: str) -> str:
    if not fields:
        return "    pass"

    lines: list[str] = []
    for field in fields.split():
        if ":" not in field:
            continue
        name, ftype = field.split(":", 1)
        sqlalchemy_type = FIELD_SQL_TYPES.get(ftype, "String(255)")
        hint = "int" if ftype == "int" else "str"
        lines.append(f"    {name}: Mapped[{hint}] = mapped_column({sqlalchemy_type})")
    return "\n".join(lines) if lines else "    pass"


def _generate_model(class_name: str, name_snake: str, fields: str) -> None:
    model_path = Path(f"app/models/{name_snake}.py")
    model_template = f"""from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer
from PythonMVC.model import BaseModel


class {class_name}(BaseModel):
    __tablename__ = '{name_snake}s'
{_build_model_columns(fields)}
"""
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model_path.write_text(model_template)
    typer.echo(f"✔ Generated model at {model_path}")


def _generate_controller(class_name: str, name_snake: str) -> None:
    controller_path = Path(f"app/controllers/{name_snake}s_controller.py")
    controller_template = f"""from PythonMVC.controller import BaseController
from starlette.requests import Request


class {class_name}sController(BaseController):
    async def index(self, request: Request):
        return self.render(request, '{name_snake}s/index.html')
"""
    controller_path.parent.mkdir(parents=True, exist_ok=True)
    controller_path.write_text(controller_template)
    typer.echo(f"✔ Generated controller at {controller_path}")


def _generate_views(name_snake: str) -> None:
    view_dir = Path(f"app/views/{name_snake}s")
    view_dir.mkdir(parents=True, exist_ok=True)
    index_view = """{% extends 'shared/layout.html' %}{% block body %}
<h1>Index</h1>
{% endblock %}"""
    (view_dir / "index.html").write_text(index_view)
    typer.echo("✔ Generated scaffold views")


def generate(kind: str, name: str, fields: str = "") -> None:
    """Generate code: model/controller/scaffold."""
    name_snake = snake_case(name)

    if kind == "model":
        _generate_model(name, name_snake, fields)
    elif kind == "controller":
        _generate_controller(name, name_snake)
    elif kind == "scaffold":
        _generate_model(name, name_snake, fields)
        _generate_controller(name, name_snake)
        _generate_views(name_snake)
    else:
        typer.echo("Unknown kind. Use: model | controller | scaffold")
