from cristalix.models import Player, FriendPlayer


class PlayersAPI:
    BASE = "/players/v1/"

    def __init__(self, pool):
        self.pool = pool

    @staticmethod
    def _chunked(items: list, size: int) -> list[list]:
        for i in range(0, len(items), size):
            yield items[i:i + size]

    async def get_player(self, nickname: str) -> Player | None:
        """Возвращает основную информацию о профиле игрока: никнейм, группу, ссылки на скины и время в игре."""
        data = await self.pool.request(
            "GET",
            self.BASE + "getProfileByName",
            params={"playerName": nickname},
        )
        return Player.from_dict(data) if data else None

    async def get_player_by_uuid(self, uuid: str) -> Player | None:
        """Возвращает основную информацию о профиле игрока: никнейм, группу, ссылки на скины и время в игре."""
        data = await self.pool.request(
            "GET",
            self.BASE + "getProfileById",
            params={"playerId": uuid},
        )
        return Player.from_dict(data) if data else None

    async def get_players(self, nicknames: list[str]) -> list[Player] | None:
        """Возвращает основную информацию о профилях игроков: никнейм, группу, ссылки на скины и время в игре."""
        data = await self.pool.request(
            "GET",
            self.BASE + "getProfilesByNames",
            json={"array": nicknames},
        )
        return [Player.from_dict(p) for p in data] if data else None

    async def get_players_by_uuid(self, uuids: list[str]) -> list[Player] | None:
        """Возвращает основную информацию о профилях игроков: никнейм, группу, ссылки на скины и время в игре."""
        data = await self.pool.request(
            "GET",
            self.BASE + "getProfilesByIds",
            json={"array": uuids},
        )
        return [Player.from_dict(p) for p in data] if data else None

    async def get_player_reactions(self, uuid: str) -> dict | None:
        """Получить количество лайков и дизлайков в профиле игрока."""
        data = await self.pool.request(
            "GET",
            self.BASE + "getProfileReactions",
            params={"playerId": uuid},
        )
        return data

    async def get_friends(self, uuid: str,
                          max_count: int | None = None,
                          extended: bool = False) -> list[FriendPlayer] | None:
        friends = await self._get_relations(uuid, "getFriends", max_count=max_count)
        if extended and friends:
            await self._populate_profiles(friends)
        return friends

    async def get_subscriptions(self, uuid: str,
                                max_count: int | None = None,
                                extended: bool = False) -> list[FriendPlayer] | None:
        subs = await self._get_relations(uuid, "getSubscriptions", max_count=max_count)
        if extended and subs:
            await self._populate_profiles(subs)
        return subs

    async def _get_relations(
        self,
        uuid: str,
        endpoint: str,
        *,
        max_count: int | None = None
    ) -> list[FriendPlayer] | None:
        relations: list[FriendPlayer] = []
        current_skip = 0
        batch_size = 100

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

            if not r:
                return None

            batch = r.get("list", [])
            total = r.get("totalCount", 0)

            if not batch:
                break

            relations.extend(
                FriendPlayer(
                    uuid=f.get("playerId"),
                    username=f.get("username"),
                    groupName=f.get("groupName"),
                    relationType=f.get("relationType"),
                )
                for f in batch
            )

            if max_count is not None and len(relations) >= max_count:
                break
            if len(relations) >= total:
                break

            current_skip += to_fetch

        return relations or None

    async def _populate_profiles(self, relations: list[FriendPlayer], batch_size: int = 50) -> None:
        """
        Обогащает FriendPlayer.profile объектами Player (батчами по batch_size).
        """
        if not relations:
            return

        for chunk in self._chunked(relations, batch_size):
            names = [r.username for r in chunk if r.username]
            if not names:
                continue

            players = await self.get_players(names)
            if not players:
                continue

            players_map = {p.username.lower(): p for p in players if p.username}

            for relation in chunk:
                relation.profile = players_map.get(relation.username.lower())
