"""
MIT License

Copyright (c) 2022 Grapphy 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING
from .beatmap import Beatmap
from .score import Score
from .enums import GameMode

if TYPE_CHECKING:
    from .types.obj import ObjectID
    from .types.user import User as UserPayload
    from .channel import ChatChannel
    from .connection import Connector


class BaseUser:
    __slots__ = (
        "id",
        "username",
        "avatar_url",
        "country_code",
        "_connector",
        "default_group",
        "is_active",
        "is_bot",
        "is_deleted",
        "is_online",
        "is_supporter",
        "pm_friends_only",
        "last_visit",
        "profile_colour",
        "cover_url",
        "has_supported",
        "join_date",
        "kudosu_available",
        "kudosu_total",
        "max_blocks",
        "max_friends",
        "post_count",
        "playmode",
        "playstyle",
        "profile_order",
        "title",
        "title_url",
        "discord",
        "twitter",
        "website",
        "location",
        "interests",
        "occupation",
    )

    if TYPE_CHECKING:
        id: ObjectID
        username: str
        avatar_url: str
        country_code: str
        _connector: Connector
        default_group: str
        last_visit: Optional[str]
        profile_colour: Optional[str]
        is_active: bool
        is_bot: bool
        is_deleted: bool
        is_online: bool
        is_supporter: bool
        pm_friends_only: bool
        cover_url: str
        has_supported: bool
        join_date: str
        kudosu_available: int
        kudosu_total: int
        max_blocks: int
        max_friends: int
        post_count: int
        playmode: object
        playstyle: List[str]
        profile_order: List[object]
        title: Optional[str]
        title_url: Optional[str]
        discord: Optional[str]
        twitter: Optional[str]
        website: Optional[str]
        location: Optional[str]
        interests: Optional[str]
        occupation: Optional[str]

    def __init__(self, *, connector: Connector, data: UserPayload) -> None:
        self._connector = connector
        self._update_data(data)

    def __repr__(self) -> str:
        return (
            f"<BaseUser id={self.id} username={self.username!r}"
            f" country={self.country_code} bot={self.is_bot}"
            f" online={self.is_online}>"
        )

    def __str__(self) -> str:
        return f"{self.username}:{self.id}"

    def __eq__(self, o: Any) -> bool:
        return isinstance(self, o) and o.id == self.id

    def __ne__(self, o: Any) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        return self.id

    def _update_data(self, data: UserPayload) -> None:
        self.id = int(data["id"])
        self.username = data["username"]
        self.avatar_url = data["avatar_url"]
        self.country_code = data["country_code"]
        self.default_group = data["default_group"]
        self.is_active = data["is_active"]
        self.is_bot = data["is_bot"]
        self.is_deleted = data["is_deleted"]
        self.is_online = data["is_online"]
        self.is_supporter = data["is_supporter"]
        self.pm_friends_only = data["pm_friends_only"]
        self.last_visit = data.get("last_visit", None)
        self.profile_colour = data.get("profile_colour", None)
        self.cover_url = data.get("cover_url", None)
        self.has_supported = data.get("has_supported", False)
        self.join_date = data.get("join_data", None)
        self.kudosu_available = data.get("kudosu_available", 0)
        self.kudosu_total = data.get("kudosu_total", 0)
        self.max_blocks = data.get("max_blocks", 0)
        self.max_friends = data.get("max_friends", 0)
        self.post_count = data.get("post_count", 0)
        self.playmode = data.get("playmode", None)
        self.playstyle = data.get("playstyle", [])
        self.profile_order = data.get("profile_order", [])
        self.title = data.get("title", None)
        self.title_url = data.get("title_url", None)
        self.discord = data.get("discord", None)
        self.twitter = data.get("twitter", None)
        self.website = data.get("website", None)
        self.location = data.get("location", None)
        self.interests = data.get("interests", None)
        self.occupation = data.get("occupation", None)

    def _to_compact_user_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "avatar_url": self.avatar_url,
            "country_code": self.country_code,
            "default_group": self.default_group,
            "last_visit": self.last_visit,
            "profile_colour": self.profile_colour,
            "is_active": self.is_active,
            "is_bot": self.is_bot,
            "is_deleted": self.is_deleted,
            "is_online": self.is_online,
            "is_supporter": self.is_supporter,
            "pm_friends_only": self.pm_friends_only,
        }


class User(BaseUser):
    def __init__(self, *, connector: Connector, data: UserPayload) -> None:
        super().__init__(connector=connector, data=data)

    @property
    def pm_channel(self) -> Optional[ChatChannel]:
        return self._connector._get_cached_pmchannel(self.id)

    async def fetch_beatmap_scores(
        self,
        beatmap: Union[ObjectID, Beatmap],
        *,
        mode: Optional[GameMode] = GameMode.Osu,
    ) -> Score:
        bid = beatmap.id if type(beatmap) is Beatmap else beatmap
        data = await self._connector.http.get_user_beatmap_score(
            bid, self.id, mode=mode
        )
        data["score"]["position"] = data["position"]
        return Score(connector=self._connector, data=data["score"])

    async def create_pm(self, message: str) -> Any:
        temp = self.pm_channel
        if temp is not None:
            return temp

        data = await self._connector.http.create_new_pm(self.id, message)
        return self._connector.create_pm_channel(self.id, data)
