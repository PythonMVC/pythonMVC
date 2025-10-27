"""Routing helpers."""

from __future__ import annotations

from typing import List, Type

from starlette.routing import Route


class ControllerFactoryError(RuntimeError):
    """Raised when we cannot instantiate the given controller."""


def resource(name: str, controller_cls: Type) -> List[Route]:
    """Build REST-style Starlette routes for a controller class."""
    try:
        controller = controller_cls()
    except Exception as exc:  # pragma: no cover - defensive guard
        raise ControllerFactoryError(f"Could not instantiate controller {controller_cls!r}") from exc

    base = f"/{name}"
    return [
        Route(base, controller.index, methods=["GET"], name=f"{name}.index"),
        Route(f"{base}/new", controller.new, methods=["GET"], name=f"{name}.new"),
        Route(base, controller.create, methods=["POST"], name=f"{name}.create"),
        Route(f"{base}/{{id}}", controller.show, methods=["GET"], name=f"{name}.show"),
        Route(f"{base}/{{id}}/edit", controller.edit, methods=["GET"], name=f"{name}.edit"),
        Route(
            f"{base}/{{id}}",
            controller.update,
            methods=["POST", "PUT", "PATCH"],
            name=f"{name}.update",
        ),
        Route(f"{base}/{{id}}", controller.destroy, methods=["DELETE"], name=f"{name}.destroy"),
    ]
