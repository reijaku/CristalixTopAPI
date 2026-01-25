import time


class RateLimiter:
    def __init__(self, rate: int, per: float = 60.0):
        self.capacity = float(rate)
        self.tokens = float(rate)
        self.per = per
        self.updated = time.monotonic()
        self._used = 0

    def acquire(self) -> bool:
        now = time.monotonic()
        elapsed = now - self.updated
        self.updated = now

        self.tokens = min(self.capacity, self.tokens + elapsed * (self.capacity / self.per))

        if self.tokens < 1:
            return False

        self.tokens -= 1
        self._used += 1
        return True

    @property
    def count(self) -> int:
        return self._used
