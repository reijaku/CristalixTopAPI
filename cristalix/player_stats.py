class PlayerStatsAPI:
    """API для работы со статистикой игроков."""
    
    def __init__(self, pool):
        self.pool = pool

    async def get_all_stats(
        self,
        player_id: str,
        *,
        game_ids: list[str] | None = None,
        seasons: str = "current"
    ) -> dict:
        """Возвращает игровую статистику игрока по всем играм одним запросом.
        
        Args:
            player_id: UUID игрока
            game_ids: Фильтр по UUID игр (можно несколько)
            seasons: Какие сезоны вернуть (current - только текущий, all - все сезоны)
            
        Returns:
            dict с ключами: playerId, privacyHidden, games
            
        Note:
            Ответ содержит все периоды: HOUR, DAY, WEEK, MONTH, QUARTER, YEAR, ALL.
            Пустые комбинации игр и режимов не возвращаются.
            Если игрок скрыл активность, вернётся privacyHidden=true и games=null.
        """
        params = [("seasons", seasons)]
        
        if game_ids:
            for game_id in game_ids:
                params.append(("gameId", game_id))
        
        data = await self.pool.request(
            "GET",
            f"/v1/api/players/{player_id}/stats",
            params=params,
        )
        return data or {"playerId": player_id, "privacyHidden": True, "games": None}

    async def get_player_stats(
        self,
        game_id: str,
        player_id: str,
        *,
        mode: str | None = None,
        sub_mode: str | None = None,
        season: str | None = None,
        period: str = "ALL",
        field: str | None = None
    ) -> dict:
        """Возвращает статистику игрока за выбранный период.
        
        Args:
            game_id: UUID игры
            player_id: UUID игрока
            mode: Режим игры
            sub_mode: Подрежим игры
            season: Сезон игры (по умолчанию текущий)
            period: Период статистики (ALL, YEAR, QUARTER, MONTH, WEEK, DAY, HOUR)
            field: Если указан — в ответе останется только это поле
            
        Returns:
            dict с ключами: playerId, gameId, mode, subMode, season, period, fields, privacyHidden
            
        Note:
            Если игрок скрыл активность, fields будет null и privacyHidden=true.
        """
        params = {"period": period}
        
        if mode:
            params["mode"] = mode
        if sub_mode:
            params["subMode"] = sub_mode
        if season:
            params["season"] = season
        if field:
            params["field"] = field
        
        data = await self.pool.request(
            "GET",
            f"/v1/api/games/{game_id}/player/{player_id}",
            params=params,
        )
        return data or {}

    async def get_player_stats_periods(
        self,
        game_id: str,
        player_id: str,
        *,
        mode: str | None = None,
        sub_mode: str | None = None,
        season: str | None = None
    ) -> dict:
        """Возвращает статистику игрока сразу по всем периодам.
        
        Args:
            game_id: UUID игры
            player_id: UUID игрока
            mode: Ключ режима
            sub_mode: Ключ субрежима
            season: Ключ сезона
            
        Returns:
            dict с ключами: playerId, gameId, mode, subMode, season, periods, privacyHidden
            periods содержит данные по HOUR, DAY, WEEK, MONTH, QUARTER, YEAR, ALL
        """
        params = {}
        
        if mode:
            params["mode"] = mode
        if sub_mode:
            params["subMode"] = sub_mode
        if season:
            params["season"] = season
        
        data = await self.pool.request(
            "GET",
            f"/v1/api/games/{game_id}/player/{player_id}/periods",
            params=params,
        )
        return data or {}

    async def get_player_position(
        self,
        game_id: str,
        player_id: str,
        field: str,
        *,
        mode: str | None = None,
        sub_mode: str | None = None,
        season: str | None = None,
        period: str = "ALL"
    ) -> dict:
        """Возвращает место игрока в топе.
        
        Args:
            game_id: UUID игры
            player_id: UUID игрока
            field: Поле, по которому ищем позицию
            mode: Режим игры
            sub_mode: Подрежим игры
            season: Сезон игры (по умолчанию текущий)
            period: Период статистики (ALL, YEAR, QUARTER, MONTH, WEEK, DAY, HOUR)
            
        Returns:
            dict с ключами: playerId, gameId, mode, subMode, season, field, period, position, privacyHidden
            
        Note:
            Если игрока нет в рейтинге, position будет -1.
        """
        params = {
            "field": field,
            "period": period
        }
        
        if mode:
            params["mode"] = mode
        if sub_mode:
            params["subMode"] = sub_mode
        if season:
            params["season"] = season
        
        data = await self.pool.request(
            "GET",
            f"/v1/api/games/{game_id}/player/{player_id}/position",
            params=params,
        )
        return data or {}