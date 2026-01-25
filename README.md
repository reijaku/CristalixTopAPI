# Cristalix API SDK

Python SDK для работы с официальным API Cristalix (Players и Statistics).

## Установка

```bash
pip install git+https://github.com/reijaku/CristalixTopAPI.git
```
## Пример использования
#### Получение информации об игроке
```python
import asyncio
from cristalix.api import CristalixAPI

async def main():
    api = CristalixAPI(token="xxx", project_key="yyy")
    player = await api.players.get_player("nickname")
    print(player.username)
    await api.close()

asyncio.run(main())
```
#### Получение статистики активности игрока в режимах за текущий день.
```python
import asyncio
from cristalix.api import CristalixAPI

async def main():
    api = CristalixAPI(token="xxx", project_key="yyy")
    activity = await api.statistics.get_player_activity('uuid')
    print(activity)
    await api.close()

asyncio.run(main())
```
