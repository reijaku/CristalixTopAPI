# Cristalix API SDK

Asynchronous Python SDK for the Cristalix public API.

Supports:
- Player profiles and relations
- Player statistics
- Rate-limited authenticated requests
- Public endpoints (search, skins, roles)
- Parsed data models with computed properties

---

## Installation

```bash
pip install git+https://github.com/reijaku/CristalixTopAPI.git
```
## Quick start
```python
import asyncio
from cristalix import CristalixAPI

async def main():
    api = CristalixAPI(
        token="YOUR_TOKEN",
        project_key="YOUR_PROJECT_KEY",
    )

    player = await api.players.get_player("Notch")
    stats = await api.statistics.get_player_statistics(player["playerId"])

    print(player)
    print(stats)

    await api.close()

asyncio.run(main())
```
## Authentication
Single account:
```python
CristalixAPI(
    token="YOUR_TOKEN",
    project_key="YOUR_PROJECT_KEY"
)
```
Multiple accounts (load balancing / rate limiting):
```python
CristalixAPI(
    accounts=[
        {"token": "...", "project_key": "..."},
        {"token": "...", "project_key": "..."},
    ],
    rate_limit=120,
)
```
## Players API
```python
player = await api.players.get_player("nickname")
player = await api.players.get_player_by_uuid(uuid)

players = await api.players.get_players(["nick1", "nick2"])
players = await api.players.get_players_by_uuid([uuid1, uuid2])

reactions = await api.players.get_player_reactions(uuid)

friends, total = await api.players.get_friends(uuid, extended=True)
subscriptions, total = await api.players.get_subscriptions(uuid)
```
## Statistics API
```python
activity = await api.statistics.get_player_activity(uuid)
stats = await api.statistics.get_player_statistics(uuid)
games = await api.statistics.list_games()
```
## PublicPlayerService (no authentication)
Public endpoints that do not require a token.
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
## Data models
Some methods return structured objects instead of raw dictionaries.
Models can be created manually from raw API responses if needed.

### Player
Represents a Cristalix player profile with computed properties.
```python
player.username
player.uuid
player.is_online
player.is_newbie
player.registration_ts
player.clean_realm
player.first_group
player.second_group
```
### DonateGroup
Represents a donation or staff group.
```python
group.key
group.name
group.staff_group
group.is_default
group.prefix_color
group.name_color
```
### FriendPlayer
Represents a player relation (friend or subscription).
```python
friend.uuid
friend.username
friend.group_name
friend.relation_type
```
## Notes
- Authenticated API methods return raw API responses (dict)

- Always close clients to release HTTP resources