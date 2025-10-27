"""Security middleware: headers, CSRF and naive rate limiting."""

from __future__ import annotations

import time
from typing import MutableMapping, Optional, Tuple

from itsdangerous import URLSafeSerializer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response

DEFAULT_SECURITY_CONFIG = {
    "hsts": True,
    "frame_deny": True,
    "xss_protect": True,
    "csrf": True,
    "rate_limit": 60,
    "secret": "change-me",
}


MutableBucket = MutableMapping[Tuple[str, int], int]


class SecurityMiddleware(BaseHTTPMiddleware):
    """Apply lightweight security controls for every request."""

    def __init__(self, app, config: Optional[dict] = None) -> None:
        super().__init__(app)
        merged = DEFAULT_SECURITY_CONFIG.copy()
        if config:
            merged.update(config)
        self.config = merged
        self.signer = URLSafeSerializer(self.config["secret"]) if self.config.get("csrf") else None
        self.bucket: MutableBucket = {}

    async def dispatch(self, request: Request, call_next):
        rate_limit = self.config.get("rate_limit")
        if rate_limit and self._rate_limited(request, rate_limit):
            return PlainTextResponse("Too Many Requests", status_code=429)

        if self.config.get("csrf") and self._is_state_changing(request):
            if not await self._validate_csrf(request):
                return PlainTextResponse("CSRF Failed", status_code=403)

        response: Response = await call_next(request)
        self._apply_security_headers(response)

        if self.config.get("csrf"):
            self._ensure_csrf_cookie(request, response)

        return response

    @staticmethod
    def _is_state_changing(request: Request) -> bool:
        return request.method in {"POST", "PUT", "PATCH", "DELETE"}

    def _rate_limited(self, request: Request, limit: int) -> bool:
        now = int(time.time() // 60)
        key = (request.client.host if request.client else "anonymous", now)
        self.bucket[key] = self.bucket.get(key, 0) + 1
        return self.bucket[key] > limit

    async def _validate_csrf(self, request: Request) -> bool:
        if not self.signer:
            return True

        token = request.headers.get("x-csrf-token")
        if not token and request.headers.get("content-type", "").startswith("application/x-www-form-urlencoded"):
            form = await request.form()
            token = form.get("_csrf")

        cookie = request.cookies.get("csrf")
        try:
            return bool(token and cookie and self.signer.loads(token) == cookie)
        except Exception:  # pragma: no cover - signer failures surface as False
            return False

    def _apply_security_headers(self, response: Response) -> None:
        if self.config.get("hsts"):
            response.headers.setdefault("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload")
        if self.config.get("frame_deny"):
            response.headers.setdefault("X-Frame-Options", "DENY")
        if self.config.get("xss_protect"):
            response.headers.setdefault("X-Content-Type-Options", "nosniff")
            response.headers.setdefault("X-XSS-Protection", "0")

    def _ensure_csrf_cookie(self, request: Request, response: Response) -> None:
        if not self.signer:
            return
        if request.cookies.get("csrf"):
            return
        token = self.signer.dumps("csrf")
        response.set_cookie("csrf", token, samesite="lax", httponly=False)
        response.headers.setdefault("X-CSRF-Token", token)
