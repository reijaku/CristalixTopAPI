from ._internal.pool import AccountPool
from ._internal.account import Account
from ._internal.http import HttpClient
from ._internal.limiter import RateLimiter

from .players import PlayersAPI
from .statistics import StatisticsAPI

BASE_URL = "https://api.cristalix.gg"
DEFAULT_HEADERS = {
    "accept": "application/json",
    "user-agent": "cristalix-client"
}


class CristalixAPI:
    def __init__(
        self,
        *,
        token: str | None = None,
        project_key: str | None = None,
        accounts: list[dict] | None = None,
        rate_limit: int = 120,
        headers: dict | None = None,
        timeout: int = 10,
    ):

        if accounts is None:
            if not token or not project_key:
                raise ValueError("Нужно указать либо token+project_key, либо accounts")
            accounts = [{"token": token, "project_key": project_key}]

        merged_headers = DEFAULT_HEADERS | (headers or {})
        http = HttpClient(merged_headers, timeout=timeout)

        acc_objects = []
        for acc in accounts:
            acc_objects.append(
                Account(
                    token=acc["token"],
                    project_key=acc["project_key"],
                    limiter=RateLimiter(rate_limit)
                )
            )

        pool = AccountPool(acc_objects, http, BASE_URL)

        self.players = PlayersAPI(pool)
        self.statistics = StatisticsAPI(pool)

        self._pool = pool

    async def close(self):
        await self._pool.close()
