from re import compile

COLOR_CODE_RE = compile(r'§.')

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
        return self._data.get("name")

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
    def __init__(self, data: dict):
        self._data = data

    @property
    def id(self) -> str:
        return self._data.get("id")

    @property
    def uuid(self) -> str:
        return self.id  # alias

    @property
    def username(self) -> str:
        return self._data.get("username")

    @property
    def last_join_ts(self) -> int:
        ts = self._data.get("lastJoinTime", "0")
        return int(int(ts) / 1000)

    @property
    def last_quit_ts(self) -> int:
        ts = self._data.get("lastQuitTime", "0")
        return int(int(ts) / 1000)

    @property
    def online_time(self) -> float:
        return float(self._data.get("onlineTime", 0.0))

    @property
    def realm(self) -> str:
        return self._data.get("realm", "")

    @property
    def first_group(self) -> DonateGroup | None:
        group = self._data.get("group")
        return DonateGroup(group) if group else None

    @property
    def second_group(self) -> DonateGroup | None:
        donate = self._data.get("donate")
        return DonateGroup(donate) if donate else None

    @property
    def is_personal(self) -> bool:
        return self.first_group.staff_group if self.first_group else False

    @property
    def is_online(self) -> bool | None:
        """
        Проверяет, онлайн ли игрок в данный момент.
        Возвращает True, False или None, если нет данных.
        """
        if self.last_quit_ts == 0 and self.last_join_ts == 0:
            return None
        if self.last_join_ts > self.last_quit_ts:
            return True
        if self.last_quit_ts - self.last_join_ts <= 3:
            return True
        return False

    @property
    def clean_realm(self) -> str:
        """Realm без цветовых кодов."""
        return COLOR_CODE_RE.sub("", self.realm)

    @property
    def registration_ts(self) -> int | None:
        try:
            parts = self.id.split('-')
            if len(parts) != 5:
                return None

            hex_timestamp = parts[2][1:] + parts[1] + parts[0]
            timestamp_int = int(hex_timestamp, 16)

            uuid_epoch_offset = 0x01B21DD213814000  # 122192928000000000
            unix_ts = (timestamp_int - uuid_epoch_offset) / 1e7
            return int(unix_ts)
        except Exception:
            return None

    @property
    def is_newbie(self) -> bool:
        """Новичок = зарегистрирован менее 3 месяцев назад."""
        if not self.registration_ts:
            return False

        three_months_sec = 90 * 24 * 60 * 60
        return (now_ts() - self.registration_ts) < three_months_sec

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
