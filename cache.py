"""Cache adapters built on Redis."""

from __future__ import annotations

import os
from typing import Optional

from redis import asyncio as aioredis


class Cache:
    """Lazy Redis client factory."""

    def __init__(self, url: Optional[str] = None) -> None:
        self.url = url or os.getenv("CACHE_URL", "redis://localhost:6379/0")
        self._client: aioredis.Redis | None = None

    async def client(self) -> aioredis.Redis:
        if self._client is None:
            self._client = aioredis.from_url(self.url)
        return self._client

