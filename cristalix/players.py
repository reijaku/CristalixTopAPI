from cristalix.models import Player, FriendPlayer


class PlayersAPI:
    BASE = "/players/v1/"

    def __init__(self, pool):
        self.pool = pool

    @staticmethod
    def _chunked(items: list, size: int) -> list[list]:
        for i in range(0, len(items), size):
            yield items[i:i + size]

    async def get_player(self, nickname: str) -> dict | None:
        """Возвращает основную информацию о профиле игрока: никнейм, группу, ссылки на скины и время в игре."""
        data = await self.pool.request(
            "GET",
            self.BASE + "getProfileByName",
            params={"playerName": nickname},
        )
        return data

    async def get_player_by_uuid(self, uuid: str) -> dict | None:
        """Возвращает основную информацию о профиле игрока: никнейм, группу, ссылки на скины и время в игре."""
        data = await self.pool.request(
            "GET",
            self.BASE + "getProfileById",
            params={"playerId": uuid},
        )
        return data

    async def get_players(self, nicknames: list[str]) -> list[dict] | None:
        """Возвращает основную информацию о профилях игроков: никнейм, группу, ссылки на скины и время в игре."""
        data = await self.pool.request(
            "GET",
            self.BASE + "getProfilesByNames",
            json={"array": nicknames},
        )
        return data

    async def get_players_by_uuid(self, uuids: list[str]) -> list[dict] | None:
        """Возвращает основную информацию о профилях игроков: никнейм, группу, ссылки на скины и время в игре."""
        data = await self.pool.request(
            "GET",
            self.BASE + "getProfilesByIds",
            json={"array": uuids},
        )
        return data

    async def get_player_reactions(self, uuid: str) -> dict | None:
        """Получить количество лайков и дизлайков в профиле игрока."""
        data = await self.pool.request(
            "GET",
            self.BASE + "getProfileReactions",
            params={"playerId": uuid},
        )
        return data

    async def get_friends(self,
                          uuid: str,
                          max_count: int | None = None,
                          extended: bool = False) -> tuple[list[dict], int]:
        friends, total = await self._get_relations(uuid, "getFriends", max_count=max_count)

        if extended and friends:
            friends = await self._populate_profiles(friends)
        return friends, total

    async def get_subscriptions(self,
                                uuid: str,
                                max_count: int | None = None,
                                extended: bool = False) -> tuple[list[dict], int]:
        subs, total = await self._get_relations(uuid, "getSubscriptions", max_count=max_count)

        if extended and subs:
            subs = await self._populate_profiles(subs)
        return subs, total

    async def _get_relations(
        self,
        uuid: str,
        endpoint: str,
        *,
        max_count: int | None = None
    ) -> tuple[list[dict], int]:
        relations: list[dict] = []
        current_skip = 0
        batch_size = 100

        total_count = 0

        while True:
            if max_count is not None:
                to_fetch = min(batch_size, max_count - len(relations))
                if to_fetch <= 0:
                    break
            else:
                to_fetch = batch_size

            params = {
                "playerId": uuid,
                "skip": current_skip,
                "limit": to_fetch,
            }

            r = await self.pool.request(
                "GET",
                self.BASE + endpoint,
                params=params,
            )

            batch = r.get("list", [])

            if not total_count:
                total_count = r.get("totalCount", 0)

            if not batch:
                break

            relations.extend(batch)

            if max_count is not None and len(relations) >= max_count:
                break
            if len(relations) >= total_count:
                break

            current_skip += to_fetch

        return relations, total_count

    async def _populate_profiles(self, relations: list[dict], batch_size: int = 50) -> list[dict]:
        if not relations:
            return []

        new_relations = []

        for chunk in self._chunked(relations, batch_size):
            names = [r.get("username") for r in chunk if r.get("username")]
            if not names:
                continue

            players = await self.get_players(names)
            if not players:
                continue
            new_relations.extend(players)

        return new_relations
