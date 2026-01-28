from ._internal.http import HttpClient
from cristalix.models import Player, DonateGroup

BASE_URL = "https://api.cristalix.gg"
BASE_TEXTURE_URL = "https://webdata.c7x.dev/textures"

class PublicPlayerService:
    """
    Публичные методы работы с игроками и их ресурсами.
    """
    def __init__(self, *, timeout: int = 10):
        self.http = HttpClient(headers={}, timeout=timeout)

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

    async def get_player_public(self, nickname: str) -> Player | None:
        r = await self.http.request(
            "GET",
            BASE_URL + "/players/v1/getProfileByName",
            params={"playerName": nickname}
        )
        if not r or r.status_code != 200:
            return None

        raw = r.json()

        if not raw:
            return None

        player = Player(
            id=raw.get("playerId"),
            username=raw.get("name"),
            realm=raw.get("realm"),
            last_join_time=raw.get("lastJoinTime"),
            last_quit_time=raw.get("lastQuitTime"),
        )

        first_group = second_group = None
        roles = raw.get("permissionContext", {}).get("roles", [])

        for role in roles:
            name = role.get("name")
            if not name or name == "PLAYER":
                continue
            if role.get("staffGroup") and not first_group:
                first_group = name
            elif not first_group:
                first_group = name
            elif not second_group:
                second_group = name

        if first_group:
            player.firstGroup = DonateGroup(key=first_group)
        if second_group:
            player.secondGroup = DonateGroup(key=second_group)

        return player

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
