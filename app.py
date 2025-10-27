"""Application bootstrap helpers."""

from __future__ import annotations

from typing import Any, Iterable, Sequence

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from starlette.routing import BaseRoute, Route
from starlette.staticfiles import StaticFiles

from .admin import mount_admin
from .security import SecurityMiddleware


def _iter_routes(routes: Sequence[BaseRoute] | None) -> Iterable[BaseRoute]:
    if not routes:
        return ()
    return routes


def create_app(settings: Any) -> Starlette:
    """Create a Starlette app configured with sensible defaults for PythonMVC."""

    # Collect routes before Starlette consumes the iterable so we can append fallback routes.
    routes = list(_iter_routes(getattr(settings, "ROUTES", ())))
    app = Starlette(debug=getattr(settings, "DEBUG", False), routes=routes)

    # Security hardening.
    app.add_middleware(SecurityMiddleware, config=getattr(settings, "SECURITY", {}))

    # Session handling.
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

    # Basic CORS setup (localhost-friendly by default).
    app.add_middleware(
        CORSMiddleware,
        allow_origins=getattr(settings, "CORS_ORIGINS", ["*"]),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    static_dir = getattr(settings, "STATIC_DIR", None)
    if static_dir:
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

    mount_admin(app)

    if not any(getattr(route, "path", "") == "/health" for route in app.router.routes):
        async def health(_: object) -> JSONResponse:
            return JSONResponse({"status": "ok"})

        app.router.routes.append(Route("/health", health, methods=["GET"], name="health"))

    return app
