class SocialAPI:
    """API для работы с социальными данными игроков."""
    
    BASE = "/v1/api/players"

    def __init__(self, pool):
        self.pool = pool

    async def get_friends(
        self,
        player_id: str,
        *,
        offset: int = 0,
        limit: int = 50,
        fields: list[str] | None = None
    ) -> dict:
        """Возвращает друзей игрока.
        
        Args:
            player_id: UUID игрока
            offset: Сколько записей пропустить (по умолчанию 0)
            limit: Максимум 100, по умолчанию 50
            fields: Список полей (total, items.playerId, items.username, items.groups, privacyHidden)
            
        Returns:
            dict с ключами: total, items, privacyHidden
            
        Note:
            Если данные скрыты настройками, список будет пустым.
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
            f"{self.BASE}/{player_id}/friends",
            params=params,
        )
        return data or {"total": 0, "items": [], "privacyHidden": True}

    async def get_subscribers(
        self,
        player_id: str,
        *,
        subscriber_type: str = "INCOMING",
        offset: int = 0,
        limit: int = 100,
        fields: list[str] | None = None
    ) -> dict:
        """Возвращает подписчиков игрока или тех, на кого подписан сам игрок.
        
        Args:
            player_id: UUID игрока
            subscriber_type: INCOMING — подписчики игрока, OUTGOING — на кого подписан сам игрок
            offset: Сколько записей пропустить (по умолчанию 0)
            limit: Максимум 100
            fields: Список полей (total, items.playerId, items.username, items.groups, privacyHidden)
            
        Returns:
            dict с ключами: total, items, privacyHidden
        """
        if limit > 100:
            raise ValueError("Лимит не может превышать 100")
        
        params: dict[str, int | str] = {
            "type": subscriber_type,
            "offset": offset,
            "limit": limit
        }
        if fields:
            params["fields"] = ",".join(fields)
        
        data = await self.pool.request(
            "GET",
            f"{self.BASE}/{player_id}/subscribers",
            params=params,
        )
        return data or {"total": 0, "items": [], "privacyHidden": True}

    async def get_history(self, player_id: str) -> dict:
        """Возвращает историю смены ника.
        
        Args:
            player_id: UUID игрока
            
        Returns:
            dict с ключами: items, privacyHidden
            items содержит: oldName, newName, changedAt
            
        Note:
            Если данные скрыты, список будет пустым.
        """
        data = await self.pool.request(
            "GET",
            f"{self.BASE}/{player_id}/history",
        )
        return data or {"items": [], "privacyHidden": True}

    async def get_location(self, player_id: str) -> dict:
        """Показывает, онлайн ли игрок и на каком реалме он находится.
        
        Args:
            player_id: UUID игрока
            
        Returns:
            dict с ключами: playerId, online, realm, realmType, privacyHidden
        """
        data = await self.pool.request(
            "GET",
            f"{self.BASE}/{player_id}/location",
        )
        return data or {"playerId": player_id, "online": False, "privacyHidden": True}

    async def get_reactions(
        self,
        player_id: str,
        *,
        reaction_type: str | None = None,
        offset: int = 0,
        limit: int = 100
    ) -> dict:
        """Возвращает игроков, которые поставили лайк или дизлайк.
        
        Args:
            player_id: UUID целевого игрока
            reaction_type: Фильтр по типу реакции (LIKE, DISLIKE). Пустое значение — оба типа
            offset: Сколько записей пропустить (по умолчанию 0)
            limit: Максимум 100
            
        Returns:
            dict с ключами: total, items
            items содержит: reactorId, username, groups, type, reactedAt
        """
        if limit > 100:
            raise ValueError("Лимит не может превышать 100")
        
        params: dict[str, int | str] = {
            "offset": offset,
            "limit": limit
        }
        if reaction_type:
            params["type"] = reaction_type
        
        data = await self.pool.request(
            "GET",
            f"{self.BASE}/{player_id}/reactions",
            params=params,
        )
        return data or {"total": 0, "items": []}