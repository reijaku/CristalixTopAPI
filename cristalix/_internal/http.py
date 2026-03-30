from curl_cffi import requests
from typing import Literal

HttpMethod = Literal[
    "GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "TRACE", "PATCH", "QUERY"
]

class HttpClient:
    def __init__(self, headers: dict, timeout: int = 10):
        self._session = requests.AsyncSession(
            headers=headers,
            timeout=timeout,
        )

    async def request(self, method: HttpMethod, url: str, **kwargs):
        return await self._session.request(method, url, **kwargs)

    async def close(self):
        await self._session.close()
