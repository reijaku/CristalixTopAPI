class RolesAPI:
    """API для работы со справочником ролей."""
    
    BASE = "/v1/api"

    def __init__(self, pool):
        self.pool = pool

    async def list_roles(self, *, fields: list[str] | None = None) -> list[dict]:
        """Возвращает список всех групп с названиями, цветами и префиксами.
        
        Args:
            fields: Список полей (name, fullName, prefix, tabPrefix, nameColor, prefixColor, 
                   tabPrefixColor, chatMessageColor, staffGroup, priority, isDefault)
            
        Returns:
            Список ролей с их параметрами
            
        Note:
            Справочник ролей можно кэшировать на 5 минут.
            Цвета приходят в формате Minecraft-кодов.
            Роли не зависят от настроек приватности.
        """
        params: dict[str, str] = {}
        if fields:
            params["fields"] = ",".join(fields)
        
        data = await self.pool.request(
            "GET",
            f"{self.BASE}/roles",
            params=params if params else None,
        )
        return data or []

    async def get_staff_counts(self) -> dict[str, int]:
        """Показывает, сколько сотрудников сейчас онлайн в каждой staff-группе.
        
        Returns:
            dict где ключ — название staff-группы, значение — количество онлайн
            
        Note:
            Данные могут обновляться с задержкой до 5 минут.
            Приватность профилей на этот endpoint не влияет.
        """
        data = await self.pool.request(
            "GET",
            f"{self.BASE}/staff/counts",
        )
        return data or {}