import asyncio
from .limiter import RateLimiter

class Account:
    def __init__(
        self,
        *,
        token: str,
        project_key: str,
        limiter: RateLimiter,
    ):
        self.token = token
        self.project_key = project_key
        self.limiter = limiter
        self._lock = asyncio.Lock()

    @property
    def auth_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    async def try_acquire(self) -> bool:
        async with self._lock:
            return self.limiter.acquire()

    @property
    def used_tokens(self) -> int:
        return self.limiter.count
