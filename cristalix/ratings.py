class RatingsAPI:
    """API для работы с глобальными рейтингами."""
    
    BASE = "/v1/api/ratings"

    def __init__(self, pool):
        self.pool = pool

    async def get_karma_top(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        fields: list[str] | None = None
    ) -> list[dict]:
        """Возвращает общий топ по карме.
        
        Args:
            offset: Сколько записей пропустить (по умолчанию 0)
            limit: Сколько записей вернуть (максимум 100)
            fields: Список полей (position, playerId, username, groups, value)
            
        Returns:
            Список записей рейтинга
            
        Note:
            Данные публичны и не скрываются приватностью.
        """
        if limit > 100:
            raise ValueError("Лимит не может превышать 100")
        
        params: dict[str, int | str] = {
            "offset": offset,
            "limit": limit
        }
        if fields:
            params["fields"] = ",".join(fields)
        
        data = await self.pool.request(
            "GET",
            f"{self.BASE}/karma",
            params=params,
        )
        return data or []

    async def get_likes_top(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        fields: list[str] | None = None
    ) -> list[dict]:
        """Возвращает общий топ по лайкам.
        
        Args:
            offset: Сколько записей пропустить (по умолчанию 0)
            limit: Сколько записей вернуть (максимум 100)
            fields: Список полей (position, playerId, username, groups, value)
            
        Returns:
            Список записей рейтинга
            
        Note:
            Данные публичны и не скрываются приватностью.
        """
        if limit > 100:
            raise ValueError("Лимит не может превышать 100")
        
        params: dict[str, int | str] = {
            "offset": offset,
            "limit": limit
        }
        if fields:
            params["fields"] = ",".join(fields)
        
        data = await self.pool.request(
            "GET",
            f"{self.BASE}/likes",
            params=params,
        )
        return data or []

    async def get_views_top(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        fields: list[str] | None = None
    ) -> list[dict]:
        """Возвращает общий топ по просмотрам профиля.
        
        Args:
            offset: Сколько записей пропустить (по умолчанию 0)
            limit: Сколько записей вернуть (максимум 100)
            fields: Список полей (position, playerId, username, groups, value)
            
        Returns:
            Список записей рейтинга
            
        Note:
            Данные публичны и не скрываются приватностью.
        """
        if limit > 100:
            raise ValueError("Лимит не может превышать 100")
        
        params: dict[str, int | str] = {
            "offset": offset,
            "limit": limit
        }
        if fields:
            params["fields"] = ",".join(fields)
        
        data = await self.pool.request(
            "GET",
            f"{self.BASE}/views",
            params=params,
        )
        return data or []