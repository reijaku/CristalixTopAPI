from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from re import compile

COLOR_CODE_RE = compile(r'§.')

def now_ts() -> int:
    from time import time
    return int(time())


@dataclass
class DonateGroup:
    key: str
    name: Optional[str] = None
    prefixColor: Optional[str] = None
    nameColor: Optional[str] = None
    staffGroup: bool = False
    is_default: bool = False


    @classmethod
    def from_dict(cls, data: dict) -> "DonateGroup":
        return cls(
            key=data['key'],
            name=data.get('name'),
            prefixColor=data.get('prefixColor'),
            nameColor=data.get('nameColor'),
            staffGroup=data.get('staffGroup', False),
            is_default=data.get('default', False),
        )

@dataclass
class Player:
    id: Optional[str] = None
    username: Optional[str] = None
    last_join_time: str | None = None
    last_quit_time: str | None = None
    online_time: float = 0.0
    friends: list['FriendPlayer'] = field(default_factory=list)
    subscriptions: list['FriendPlayer'] = field(default_factory=list)
    first_group: Optional['DonateGroup'] = None
    second_group: Optional['DonateGroup'] = None
    realm: str | None = None

    @staticmethod
    def iso_to_ts(iso: str) -> int:
        if not iso:
            return 0
        iso = iso.replace("Z", "+00:00")
        return int(datetime.fromisoformat(iso).timestamp())

    @property
    def last_join_ts(self) -> int:
        return self.iso_to_ts(self.last_join_time)

    @property
    def last_quit_ts(self) -> int:
        return self.iso_to_ts(self.last_quit_time)

    @property
    def is_online(self) -> Optional[bool]:
        """Проверяет, онлайн ли игрок в данный момент"""
        if self.last_quit_ts == 0 and self.last_join_ts == 0:
            return None
        if self.last_join_ts > self.last_quit_ts:
            return True
        if self.last_quit_ts - self.last_join_ts <= 3:
            return True
        return False

    @property
    def online_status(self) -> str:
        if self.is_online is None:
            return '❓'
        elif self.is_online:
            return '🟢'
        elif not self.is_online:
            return '🔴'

    @property
    def friend_count(self) -> int:
        return len(self.friends)

    @property
    def sub_count(self) -> int:
        return len(self.subscriptions)

    @staticmethod
    def convert_seconds_to_rounded(seconds: int) -> str:
        if seconds <= 0:
            return "0 с."

        minutes = seconds // 60
        hours = minutes // 60
        days = hours // 24

        if days > 0:
            return f"{days} д."
        elif hours > 0:
            return f"{hours} ч."
        elif minutes > 0:
            return f"{minutes} м."
        else:
            return f"{seconds} с."

    @property
    def time_since_last_online(self) -> Optional[str]:
        if self.is_online or not self.last_quit_ts:
            return 'Неизвестно'
        return f'{self.convert_seconds_to_rounded(now_ts() - self.last_quit_ts)} назад'

    @property
    def current_online_duration(self) -> Optional[str]:
        if not self.is_online or not self.last_join_ts:
            return 'Неизвестно'
        return self.convert_seconds_to_rounded(now_ts() - self.last_join_ts)

    @property
    def get_realm(self) -> str:
        if not self.realm:
            return ""
        return COLOR_CODE_RE.sub('', self.realm)

    @property
    def registration_ts(self) -> int | None:
        if not self.id:
            return None
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
    def is_newbie(self) -> Optional[bool]:
        """
        Проверяет, новичок ли игрок.
        Новичок = зарегистрирован менее 3 месяцев назад.
        """
        if not self.registration_ts:
            return None  # Неизвестно

        three_months_sec = 90 * 24 * 60 * 60
        return (now_ts() - self.registration_ts) < three_months_sec

    @classmethod
    def from_dict(cls, data: dict):
        group = data.get('group')
        donate = data.get('donate')

        return cls(
            id=data.get('id'),
            username=data.get('username'),
            last_join_time=data.get('lastJoinTime', None),
            last_quit_time=data.get('lastQuitTime', None),
            online_time=float(data.get('onlineTime', 0.0)),
            realm=data.get('realm', None),
            first_group=DonateGroup.from_dict(group) if group else None,
            second_group=DonateGroup.from_dict(donate) if donate else None,
        )

@dataclass
class FriendPlayer:
    uuid: str
    username: str
    groupName: str
    relationType: str

    profile: Optional[Player] = None
