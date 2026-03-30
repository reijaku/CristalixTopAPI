# Cristalix API SDK

Асинхронная Python библиотека для работы с публичным API Cristalix.

Возможности:
- Профили игроков и социальные связи
- Статистика игроков
- Аутентифицированные запросы с rate limiting
- Публичные эндпоинты (поиск, скины, роли)
- Удобные модели данных с вычисляемыми свойствами

---

## Установка

```bash
pip install git+https://github.com/reijaku/CristalixTopAPI.git
```
## Быстрый старт
```python
import asyncio
from cristalix import CristalixAPI, Player

async def main():
    api = CristalixAPI(
        token="YOUR_TOKEN",
        project_key="YOUR_PROJECT_KEY",
    )

    # Получаем данные игрока
    player_data = await api.players.get_player("Notch")
    player = Player(player_data)
    
    # Используем удобные свойства модели
    print(f"Username: {player.username}")
    print(f"Online: {player.is_online}")
    print(f"Newbie: {player.is_newbie}")
    
    # Получаем статистику
    stats = await api.statistics.get_player_statistics(player.uuid)
    print(stats)

    await api.close()

asyncio.run(main())
```
## Аутентификация
Один аккаунт:
```python
CristalixAPI(
    token="YOUR_TOKEN",
    project_key="YOUR_PROJECT_KEY"
)
```
Несколько аккаунтов (балансировка нагрузки / rate limiting):
```python
CristalixAPI(
    accounts=[
        {"token": "...", "project_key": "..."},
        {"token": "...", "project_key": "..."},
    ],
    rate_limit=120,
)
```
## API игроков
```python
# Получить игрока (возвращает dict | None)
player = await api.players.get_player("nickname")
player = await api.players.get_player_by_uuid(uuid)

# Получить несколько игроков (возвращает list[dict], пустой список если нет данных)
players = await api.players.get_players(["nick1", "nick2"])
players = await api.players.get_players_by_uuid([uuid1, uuid2])

# Реакции профиля
reactions = await api.players.get_player_reactions(uuid)

# Друзья и подписчики (возвращает tuple: список и общее количество)
friends, total = await api.players.get_friends(uuid, max_count=50, extended=True)
subscriptions, total = await api.players.get_subscriptions(uuid, max_count=100)
```
## API статистики
```python
activity = await api.statistics.get_player_activity(uuid)
stats = await api.statistics.get_player_statistics(uuid)
games = await api.statistics.list_games()
```
## PublicPlayerService (без аутентификации)
Публичные эндпоинты, не требующие токена.
```python
import asyncio
from cristalix import PublicPlayerService

async def main():
    service = PublicPlayerService()

    player = await service.get_player_public("nickname")
    roles = await service.list_roles()

    skin = await service.get_skin(player.uuid)
    cape = await service.get_cape(player.uuid)

    await service.close()

asyncio.run(main())
```
## Модели данных
API методы возвращают сырые dict, но вы можете обернуть их в модели для удобства.

### Player
Модель игрока с вычисляемыми свойствами.
```python
from cristalix import Player

player_data = await api.players.get_player("nickname")
player = Player(player_data)  # Принимает dict | None

# Основные свойства
player.username          # str
player.uuid              # str (alias для id)
player.id                # str

# Статус и активность
player.is_online         # bool | None
player.is_newbie         # bool (зарегистрирован < 3 месяцев)
player.online_time       # float (секунды)
player.last_join_ts      # int (unix timestamp)
player.last_quit_ts      # int (unix timestamp)
player.registration_ts   # int | None (unix timestamp)

# Сервер и группы
player.realm             # str (с цветовыми кодами)
player.clean_realm       # str (без цветовых кодов)
player.first_group       # DonateGroup | None
player.second_group      # DonateGroup | None
player.is_personal       # bool (является ли персоналом)

# Преобразование
player.to_dict()         # dict (копия исходных данных)
```
### DonateGroup
Представляет донат-группу или группу персонала.
```python
group.key
group.name
group.staff_group
group.is_default
group.prefix_color
group.name_color
```
### FriendPlayer
Представляет связь с игроком (друг или подписчик).
```python
friend.uuid
friend.username
friend.group_name
friend.relation_type
```
## Важные замечания

### Возвращаемые типы
- `get_player()`, `get_player_by_uuid()` → `dict | None`
- `get_players()`, `get_players_by_uuid()` → `list[dict]` (пустой список если нет данных)
- `get_friends()`, `get_subscriptions()` → `tuple[list[dict], int]` (список и total count)
- Все методы Statistics API → `dict | None` или `list[dict]`

### Модели данных
- `Player(data)` принимает `dict | None`, безопасно обрабатывает None
- Используйте модели для удобного доступа к свойствам
- Модели не делают дополнительных API запросов

### Ресурсы
- Всегда закрывайте клиенты: `await api.close()` и `await service.close()`