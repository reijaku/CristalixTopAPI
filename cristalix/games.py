class GamesAPI:
    """API для работы с играми и режимами."""
    
    BASE = "/v1/api/games"

    def __init__(self, pool):
        self.pool = pool

    async def list_games(self) -> list[dict]:
        """Возвращает список активных игр с режимами, полями статистики и сезонами.
        
        Returns:
            Список игр с полной информацией о режимах и сезонах
            
        Note:
            Результат можно кэшировать на 10 минут.
        """
        data = await self.pool.request(
            "GET",
            self.BASE,
        )
        return data or []

    async def get_leaderboard(
        self,
        game_id: str,
        field: str,
        *,
        mode: str | None = None,
        sub_mode: str | None = None,
        season: str | None = None,
        period: str = "ALL",
        offset: int = 0,
        limit: int = 100,
        trends: bool = False,
        fields: list[str] | None = None
    ) -> list[dict]:
        """Возвращает топ игроков по выбранному полю.
        
        Args:
            game_id: UUID игры
            field: Поле для сортировки (из GET /games)
            mode: Режим игры
            sub_mode: Подрежим игры
            season: Сезон игры (по умолчанию текущий)
            period: Период статистики (ALL, YEAR, QUARTER, MONTH, WEEK, DAY, HOUR)
            offset: Сколько записей пропустить (по умолчанию 0)
            limit: Сколько записей вернуть (максимум 100)
            trends: Добавить объект trends с расчётом динамики
            fields: Список полей для возврата (position, playerId, username, value, groups, social, trends)
            
        Returns:
            Список записей лидерборда
            
        Note:
            Игроки со скрытой игровой активностью не попадают в список.
            trends=true увеличивает время ответа.
        """
        if limit > 100:
            raise ValueError("Лимит не может превышать 100")
        
        params = {
            "field": field,
            "period": period,
            "offset": offset,
            "limit": limit,
            "trends": str(trends).lower()
        }
        
        if mode:
            params["mode"] = mode
        if sub_mode:
            params["subMode"] = sub_mode
        if season:
            params["season"] = season
        if fields:
            params["fields"] = ",".join(fields)
        
        data = await self.pool.request(
            "GET",
            f"{self.BASE}/{game_id}/leaderboard",
            params=params,
        )
        return data or []

    async def get_leaderboard_rich(
        self,
        game_id: str,
        field: str,
        *,
        mode: str | None = None,
        sub_mode: str | None = None,
        season: str | None = None,
        period: str = "ALL",
        offset: int = 0,
        limit: int = 100,
        fields: list[str] | None = None
    ) -> list[dict]:
        """Возвращает топ, динамику и значения по всем периодам одним запросом.
        
        Args:
            game_id: UUID игры
            field: Поле для сортировки
            mode: Режим игры
            sub_mode: Подрежим игры
            season: Сезон игры (по умолчанию текущий)
            period: Период статистики (ALL, YEAR, QUARTER, MONTH, WEEK, DAY, HOUR)
            offset: Сколько записей пропустить (по умолчанию 0)
            limit: Сколько записей вернуть (максимум 100)
            fields: Список полей для возврата (position, playerId, username, value, groups, social, trends)
            
        Returns:
            Список записей с расширенной информацией (trends, fieldsByPeriod, periodEnding)
            
        Note:
            Запрос тяжелее обычного. Используйте когда нужны данные по всем периодам.
            periodEnding — время окончания периода в unix-миллисекундах. Для period=ALL возвращается -1.
        """
        if limit > 100:
            raise ValueError("Лимит не может превышать 100")
        
        params = {
            "field": field,
            "period": period,
            "offset": offset,
            "limit": limit
        }
        
        if mode:
            params["mode"] = mode
        if sub_mode:
            params["subMode"] = sub_mode
        if season:
            params["season"] = season
        if fields:
            params["fields"] = ",".join(fields)
        
        data = await self.pool.request(
            "GET",
            f"{self.BASE}/{game_id}/leaderboard/rich",
            params=params,
        )
        return data or []