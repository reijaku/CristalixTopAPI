from typing import Literal

class StatisticsAPI:
    BASE = "/statistics/v1/"

    def __init__(self, pool):
        self.pool = pool

    async def get_player_activity(self, uuid: str) -> dict | None:
        """Статистика активности игрока в режимах за текущий день."""
        data = await self.pool.request(
            "GET",
            self.BASE + "getProfileActivityStatistics",
            params={"playerId": uuid},
        )
        return data

    async def get_player_lifetime_statistics(self, uuid: str) -> list[dict]:
        """Полная статистика игрока по всем играм, в которые он когда-либо играл за все периоды которые доступны."""
        data = await self.pool.request(
            "GET",
            self.BASE + "getAllProfileStatistics",
            params={"playerId": uuid},
        )
        return data

    async def get_player_statistics(self, uuid: str) -> dict | None:
        """Полная статистика игрока по всем играм, в которые он когда-либо играл."""
        data = await self.pool.request(
            "GET",
            self.BASE + "getProfileStatistics",
            params={"playerId": uuid},
        )
        return data

    async def list_games(self) -> dict | None:
        """Получить список всех доступных игр, режимов и полей статистики для формирования запросов."""
        data = await self.pool.request(
            "GET",
            self.BASE + "gamesList"
        )
        return data

    async def get_leaderboard(self,
                              time: Literal['HOUR', 'DAY', 'WEEK', 'MONTH', 'QUARTER', 'YEAR', 'ALL'],
                              game_id: str,
                              mode_key: str,
                              sub_mode_key: str,
                              sort_field: str,
                              season_key: str):
        """НЕ РАБОТАЕТ Получить топ игроков по определенному параметру, режиму и временному промежутку."""
        # data = await self.pool.request(
        #     "GET",
        #     self.BASE + "readByTimeRating"
        # )
        return None
