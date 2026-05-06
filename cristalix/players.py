class PlayersAPI:
    BASE = "/v1/api/players/"

    def __init__(self, pool):
        self.pool = pool

    async def get_player(self, nickname: str, *, fields: list[str] | None = None, lite: bool = False) -> dict | None:
        """Возвращает профиль игрока по нику.
        
        Args:
            nickname: Ник игрока
            fields: Список полей для возврата (playerId, name, groups, status, stats, social, customization, relation, version, createdAt, updatedAt)
            lite: Облегчённый формат (только playerId, name, status, relation)
        """
        params = {"lite": str(lite).lower()}
        if fields:
            params["fields"] = ",".join(fields)
        
        data = await self.pool.request(
            "GET",
            self.BASE + f"by-name/{nickname}",
            params=params,
        )
        return data

    async def get_player_by_uuid(self, uuid: str, *, fields: list[str] | None = None, lite: bool = False) -> dict | None:
        """Возвращает профиль игрока по UUID.
        
        Args:
            uuid: UUID игрока
            fields: Список полей для возврата (playerId, name, groups, status, stats, social, customization, relation, version, createdAt, updatedAt)
            lite: Облегчённый формат (только playerId, name, status, relation)
        """
        params = {"lite": str(lite).lower()}
        if fields:
            params["fields"] = ",".join(fields)
        
        data = await self.pool.request(
            "GET",
            self.BASE + uuid,
            params=params,
        )
        return data

    async def get_players(self, nicknames: list[str], *, fields: list[str] | None = None, lite: bool = False) -> dict:
        """Массовое получение профилей по никам (1-200 ников).
        
        Args:
            nicknames: Список ников (1-200 шт, длина каждого 2-32 символа)
            fields: Список полей для возврата
            lite: Облегчённый формат
            
        Returns:
            dict с ключами: requested, found, notFound, items
        """
        if not nicknames or len(nicknames) > 200:
            raise ValueError("Количество ников должно быть от 1 до 200")
        
        params = {"lite": str(lite).lower()}
        if fields:
            params["fields"] = ",".join(fields)
        
        data = await self.pool.request(
            "POST",
            self.BASE + "batch/names",
            params=params,
            json={"names": nicknames},
        )
        return data or {"requested": 0, "found": 0, "notFound": [], "items": []}

    async def get_players_by_uuid(self, uuids: list[str], *, fields: list[str] | None = None, lite: bool = False) -> dict:
        """Массовое получение профилей по UUID (1-200 UUID).
        
        Args:
            uuids: Список UUID (1-200 шт)
            fields: Список полей для возврата
            lite: Облегчённый формат
            
        Returns:
            dict с ключами: requested, found, notFound, items
        """
        if not uuids or len(uuids) > 200:
            raise ValueError("Количество UUID должно быть от 1 до 200")
        
        params = {"lite": str(lite).lower()}
        if fields:
            params["fields"] = ",".join(fields)
        
        data = await self.pool.request(
            "POST",
            self.BASE + "batch",
            params=params,
            json={"ids": uuids},
        )
        return data or {"requested": 0, "found": 0, "notFound": [], "items": []}

    async def search(self, query: str, *, limit: int = 20, fields: list[str] | None = None, lite: bool = False) -> list[dict]:
        """Поиск игроков по началу ника (автокомплит).
        
        Args:
            query: Префикс ника (минимум 1 символ)
            limit: Количество результатов (1-20, по умолчанию 20)
            fields: Список полей для возврата (playerId, name, groups, status, stats, social, customization, relation, version, createdAt, updatedAt)
            lite: Облегчённый формат (только playerId, name, status, groups)
            
        Returns:
            Список найденных профилей
            
        Note:
            У поиска отдельный лимит: 60 запросов в минуту на project_key.
            Запросы поиска не тратят общий лимит API.
        """
        if not query:
            raise ValueError("Запрос не может быть пустым")
        if limit < 1 or limit > 20:
            raise ValueError("Лимит должен быть от 1 до 20")
        
        params = {
            "q": query,
            "limit": limit,
            "lite": str(lite).lower()
        }
        if fields:
            params["fields"] = ",".join(fields)
        
        data = await self.pool.request(
            "GET",
            self.BASE + "search",
            params=params,
        )
        return data or []

    