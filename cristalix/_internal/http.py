from curl_cffi import requests


class HttpClient:
    def __init__(self, headers: dict, timeout: int = 10):
        self._session = requests.AsyncSession(
            headers=headers,
            timeout=timeout,
        )

    async def request(self, method: str, url: str, **kwargs):
        return await self._session.request(method, url, **kwargs)

    async def close(self):
        await self._session.close()
