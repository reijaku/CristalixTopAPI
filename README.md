# Cristalix API SDK

Python SDK для работы с официальным API Cristalix (Players и Statistics).

## Установка

```bash
pip install cristalix
```
Пример использования
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