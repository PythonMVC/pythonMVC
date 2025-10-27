"""Controller base classes."""

from __future__ import annotations

from typing import Any, Dict, Optional

from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.templating import Jinja2Templates


class BaseController:
    """Base controller with Rails-inspired conventions for template rendering."""

    def __init__(self, templates_dir: str = "app/views") -> None:
        self.templates = Jinja2Templates(directory=templates_dir)

    async def before_action(self, request: Request) -> None:  # pragma: no cover - hooks are user-defined
        """Override for per-request setup."""

    async def after_action(self, request: Request, response: Response) -> Response:  # pragma: no cover
        """Override for teardown/response decoration."""
        return response

    def render(self, request: Request, template: str, context: Optional[Dict[str, Any]] = None) -> Response:
        payload = {"request": request}
        if context:
            payload.update(context)
        return self.templates.TemplateResponse(template, payload)

    def redirect(self, url: str, status_code: int = 302) -> RedirectResponse:
        return RedirectResponse(url=url, status_code=status_code)

    # Default REST actions (override as needed)
    async def index(self, request: Request) -> Response:
        return self.render(request, "shared/placeholder.html", {"action": "index"})

    async def new(self, request: Request) -> Response:
        return self.render(request, "shared/placeholder.html", {"action": "new"})

    async def create(self, request: Request) -> Response:
        return self.redirect("/")

    async def show(self, request: Request) -> Response:
        return self.render(request, "shared/placeholder.html", {"action": "show"})

    async def edit(self, request: Request) -> Response:
        return self.render(request, "shared/placeholder.html", {"action": "edit"})

    async def update(self, request: Request) -> Response:
        return self.redirect("/")

    async def destroy(self, request: Request) -> Response:
        return self.redirect("/")

