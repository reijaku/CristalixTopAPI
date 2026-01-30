from ._internal.http import HttpClient

BASE_URL = "https://api.cristalix.gg"
BASE_TEXTURE_URL = "https://webdata.c7x.dev/textures"

class PublicPlayerService:
    """
    Публичные методы работы с игроками и их ресурсами.
    """
    def __init__(self, *, timeout: int = 10):
        self.http = HttpClient(headers={}, timeout=timeout)

    async def get_web_profiles_by_ids(self, uuids: list[str]) -> list[dict]:
        r = await self.http.request(
            "POST",
            BASE_URL + "/players/v1/getWebProfilesByIds",
            json={"array": uuids}
        )
        if not r or r.status_code != 200:
            return []

        raw = r.json()

        return raw

    async def search(self, pattern: str) -> list[dict]:
        r = await self.http.request(
            "GET",
            BASE_URL + "/players/v1/search",
            params={"pattern": pattern}
        )
        if not r or r.status_code != 200:
            return []

        raw = r.json()

        return raw

    async def list_roles(self):
        r = await self.http.request(
            "GET",
            BASE_URL + "/players/v1/getAllRoles"
        )
        if not r or r.status_code != 200:
            return None

        raw = r.json()

        if not raw:
            return None

        return raw

    async def get_player_public(self, nickname: str) -> dict | None:
        r = await self.http.request(
            "GET",
            BASE_URL + "/players/v1/getProfileByName",
            params={"playerName": nickname}
        )
        if not r or r.status_code != 200:
            return None

        data = r.json()

        return data

    async def get_skin(self, uuid: str) -> bytes | None:
        url = f"{BASE_TEXTURE_URL}/skin/{uuid}"
        r = await self.http.request("GET", url)
        return r.content if r.status_code == 200 else None

    async def get_cape(self, uuid: str) -> bytes | None:
        url = f"{BASE_TEXTURE_URL}/cape/{uuid}"
        r = await self.http.request("GET", url)
        return r.content if r.status_code == 200 else None

    async def close(self):
        await self.http.close()
