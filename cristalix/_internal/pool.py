import asyncio
from .account import Account
from .http import HttpClient
from cristalix.errors import Unauthorized, NotFound, ApiError


class AccountPool:
    BASE_URL = 'https://api.cristalix.gg'

    def __init__(self, accounts: list[Account], http: HttpClient, base_url: str):
        if not accounts:
            raise ValueError("AccountPool requires at least one account")
        self._accounts = accounts
        self.http = http
        self.base_url = base_url

    async def request(
        self,
        method: str,
        path: str,
        *,
        params=None,
        json=None,
    ):
        acc = await self.acquire()

        params = params or {}
        params["project_key"] = acc.project_key

        r = await self.http.request(
            method,
            self.BASE_URL + path,
            params=params,
            json=json,
            headers=acc.auth_headers,
        )

        if r.status_code == 401:
            raise Unauthorized()
        if r.status_code == 404:
            raise NotFound()
        if r.status_code >= 400:
            raise ApiError(r.text)

        try:
            return r.json()
        except Exception as e:
            raise ApiError("Invalid JSON response") from e

    async def acquire(self) -> Account:
        while True:
            for acc in sorted(self._accounts, key=lambda a: a.used_tokens):
                if await acc.try_acquire():
                    return acc

            await asyncio.sleep(0.01)

    async def close(self):
        await self.http.close()
