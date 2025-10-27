"""Minimal admin surface for inspecting registered models."""

from __future__ import annotations

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette.templating import Jinja2Templates

from .model import BaseModel

templates = Jinja2Templates(directory="app/views")


async def admin_index(request: Request) -> HTMLResponse:
    models = [mapper for mapper in BaseModel.registry.mappers]
    return templates.TemplateResponse("admin/index.html", {"request": request, "models": models})


def mount_admin(app: Starlette) -> None:
    """Register the admin route if not already mounted."""
    if any(getattr(route, "path", "").startswith("/admin") for route in app.router.routes):
        return
    app.router.routes.append(Route("/admin", admin_index, name="admin.index"))
