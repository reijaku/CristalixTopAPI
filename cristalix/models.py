from re import compile

COLOR_CODE_RE = compile(r"§.")

def now_ts() -> int:
    from time import time
    return int(time())

class DonateGroup:
    def __init__(self, data: dict):
        self._data = data

    @property
    def key(self) -> str:
        return self._data.get("key", "")

    @property
    def name(self) -> str:
        return self._data.get("name", "")

    @property
    def prefix_color(self) -> str | None:
        return self._data.get("prefixColor")

    @property
    def name_color(self) -> str | None:
        return self._data.get("nameColor")

    @property
    def staff_group(self) -> bool:
        return self._data.get("staffGroup", False)

    @property
    def is_default(self) -> bool:
        return self._data.get("default", False)

    def to_dict(self) -> dict:
        return self._data.copy()

class Player:
    """Модель игрока для API v1"""
    
    def __init__(self, data: dict | None):
        self._data = data if data is not None else {}

    def __bool__(self) -> bool:
        return bool(self._data)

    @property
    def id(self) -> str:
        """UUID игрока"""
        return self._data.get("playerId", "")

    @property
    def uuid(self) -> str:
        """UUID игрока (алиас для id)"""
        return self.id

    @property
    def username(self) -> str:
        """Ник игрока"""
        return self._data.get("name", "")

    @property
    def registered_at(self) -> str:
        """ISO timestamp регистрации"""
        return self._data.get("registeredAt", "")

    @property
    def registration_ts(self) -> int | None:
        """Unix timestamp регистрации"""
        registered_at = self.registered_at
        if registered_at:
            from datetime import datetime
            try:
                dt = datetime.fromisoformat(registered_at.replace('Z', '+00:00'))
                return int(dt.timestamp())
            except:
                pass
        return None

    @property
    def is_newbie(self) -> bool:
        """Новичок = зарегистрирован менее 3 месяцев назад"""
        if not self.registration_ts:
            return False
        three_months_sec = 90 * 24 * 60 * 60
        return (now_ts() - self.registration_ts) < three_months_sec

    @property
    def last_seen_online(self) -> str:
        """ISO timestamp последнего онлайна"""
        social = self._data.get("social")
        if not social or not isinstance(social, dict):
            return ""
        return social.get("lastSeenOnline", "")

    @property
    def last_seen_ts(self) -> int:
        """Unix timestamp последнего онлайна"""
        last_seen = self.last_seen_online
        if last_seen:
            from datetime import datetime
            try:
                dt = datetime.fromisoformat(last_seen.replace('Z', '+00:00'))
                return int(dt.timestamp())
            except:
                pass
        return 0

    @property
    def realm(self) -> str:
        """Текущий реалм (может быть пустым если privacyHidden)"""
        status = self._data.get("status")
        if not status or not isinstance(status, dict):
            return ""
        return status.get("realm", "")

    @property
    def realm_type(self) -> str:
        """Тип реалма (LW, SW и т.д.)"""
        status = self._data.get("status")
        if not status or not isinstance(status, dict):
            return ""
        return status.get("realmType", "")

    @property
    def clean_realm(self) -> str:
        """Realm без цветовых кодов"""
        return COLOR_CODE_RE.sub("", self.realm)

    @property
    def staff_group(self) -> str:
        """Staff группа (HELPER, MODERATOR, ADMIN и т.д.)"""
        groups = self._data.get("groups")
        if not groups or not isinstance(groups, dict):
            return "PLAYER"
        return groups.get("staff", "PLAYER")

    @property
    def donate_group(self) -> str:
        """Донат группа (MVP, PREMIUM_PLUS, GOD и т.д.)"""
        groups = self._data.get("groups")
        if not groups or not isinstance(groups, dict):
            return "PLAYER"
        return groups.get("donate", "PLAYER")

    @property
    def display_group(self) -> str:
        """Отображаемая группа (приоритетная)"""
        groups = self._data.get("groups")
        if not groups or not isinstance(groups, dict):
            return "PLAYER"
        return groups.get("display", "PLAYER")

    @property
    def first_group(self) -> DonateGroup | None:
        """Первая группа (display)"""
        display = self.display_group
        if display and display != "PLAYER":
            return DonateGroup({"key": display, "name": display})
        return None

    @property
    def second_group(self) -> DonateGroup | None:
        """Вторая группа (donate)"""
        donate = self.donate_group
        if donate and donate != "PLAYER":
            return DonateGroup({"key": donate, "name": donate})
        return None

    @property
    def is_personal(self) -> bool:
        """Является ли игрок персоналом"""
        return self.staff_group != "PLAYER"

    @property
    def is_online(self) -> bool | None:
        """Онлайн ли игрок (None если скрыто приватностью)"""
        status = self._data.get("status")
        if not status or not isinstance(status, dict):
            return None
        if "online" in status:
            return status.get("online")
        if status.get("privacyHidden"):
            return None
        return None

    @property
    def privacy_hidden(self) -> bool:
        """Скрыл ли игрок свой онлайн-статус"""
        status = self._data.get("status")
        if not status or not isinstance(status, dict):
            return False
        return status.get("privacyHidden", False)

    @property
    def likes(self) -> int:
        """Количество лайков"""
        stats = self._data.get("stats")
        if not stats or not isinstance(stats, dict):
            return 0
        return stats.get("likes", 0)

    @property
    def dislikes(self) -> int:
        """Количество дизлайков"""
        stats = self._data.get("stats")
        if not stats or not isinstance(stats, dict):
            return 0
        return stats.get("dislikes", 0)

    @property
    def score(self) -> int:
        """Карма (likes - dislikes)"""
        stats = self._data.get("stats")
        if not stats or not isinstance(stats, dict):
            return self.likes - self.dislikes
        return stats.get("score", self.likes - self.dislikes)

    @property
    def views(self) -> int:
        """Просмотры профиля"""
        stats = self._data.get("stats")
        if not stats or not isinstance(stats, dict):
            return 0
        return stats.get("views", 0)

    @property
    def prefix(self) -> str:
        """Префикс игрока с цветовыми кодами"""
        social = self._data.get("social")
        if not social or not isinstance(social, dict):
            return ""
        return social.get("prefix", "")

    @property
    def formatted_name(self) -> str:
        """Отформатированное имя с префиксом и цветами"""
        social = self._data.get("social")
        if not social or not isinstance(social, dict):
            return self.username
        return social.get("formattedName", self.username)

    def to_dict(self) -> dict:
        return self._data.copy()

class FriendPlayer:
    def __init__(self, data: dict):
        self._data = data

    @property
    def uuid(self) -> str:
        return self._data.get("uuid", "")

    @property
    def username(self) -> str:
        return self._data.get("username", "")

    @property
    def group_name(self) -> str:
        return self._data.get("groupName", "")

    @property
    def relation_type(self) -> str:
        return self._data.get("relationType", "")

    def to_dict(self) -> dict:
        return self._data.copy()
