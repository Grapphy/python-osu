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

from typing import Any, Dict, Union, Optional, TYPE_CHECKING

from .beatmap import Beatmap, BeatmapPlaycount
from .beatmapset import Beatmapset
from .score import Score
from .enums import GameMode, BeatmapType
from .kudosu import KudosuHistory
from .event import Event

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
    """Representation of an osu! User.

    Contains data from a UserCompact/User.

    Operations:
        (x == y): Compares if two osu Users are equal.
        (x != y): Compares if two osu Users are not equal.
        (hash(x)): Returns User's hash.
        (str(x)): Returns User's username.

    Attributes:
        id (:obj:`int`): The user's unique ID.
        username (:obj:`str`): The user's username.
        avatar_url (:obj:`str`): The user's avatar url (profile picture).
        country_code (:obj:`str`): The user's country code.
        default_group (:obj:`str`): Default group for the user.
        is_active (:obj:`bool`): Defines if the user was online in
            the last months.
        is_bot (:obj:`bool`): Specifies if the user is a bot or a real user.
        is_deleted (:obj:`bool`): Specifies if the user no longer exists.
        is_online (:obj:`bool`): Specifies if the user is online.
        is_supporter (:obj:`bool`): Specifies if the user is a supporter.
        pm_friends_only (:obj:`bool`): Specifies if the user
            can receive messages.
        last_visit (:obj:`str`, optional): Shows user's last visit to osu.
        profile_colour (:obj:`str`, optional): Shows user's profile color.
        cover_url (:obj:`str`): The user's banner url.
        has_supported (:obj:`bool`): Specifies if the users was supported.
        join_date (:obj:`str`): User's registration date.
        kudosu_available (:obj:`int`): Specifies if kudosu
            history is available.
        kudosu_total (:obj:`int`): Total amount of kudosu items.
        max_blocks (:obj:`int`): Max number of blocks availables.
        max_friends (:obj:`int`): Max number of friends availables.
        post_count (:obj:`int`): Forum posts count from the user.
        playmode (:obj:`pyosu.GameMode`): User's default game mode.
        playstyle (:obj:`list`): User's play styles (keyboard, mouse, etc.)
        profile_order (:obj:`list`): User's profile orders.
        title (:obj:`str`, optional): User's title.
        title_url (:obj:`str`, optional): User's title url.
        discord (:obj:`str`, optional): User's discord username.
        twitter (:obj:`str`, optional): User's twitter username.
        website (:obj:`str`, optional): User's personal website url.
        location (:obj:`str`, optional): User's location.
        interests (:obj:`str`, optional): User's personal interests.
        occupation (:obj:`str`, optional): User's job/occupation.

    """

    def __init__(self, *, connector: Connector, data: UserPayload) -> None:
        super().__init__(connector=connector, data=data)

    @property
    def pm_channel(self) -> Optional[ChatChannel]:
        """Optional[:obj:`pyosu.ChatChannel`]: User Private Channel
        if there is one available.
        """
        return self._connector._get_cached_pmchannel(self.id)

    async def fetch_beatmap_scores(
        self,
        beatmap: Union[ObjectID, Beatmap],
        *,
        mode: Optional[GameMode] = GameMode.Osu,
    ) -> Score:
        """Fetchs user score from a beatmap. It can be a pyosu.Beatmap
        object or a beatmap ID. Returns a Score.

        Args:
            beatmap (:obj:`Union[pyosu.ObjectID, pyosu.Beatmap]`):
                A given beatmap, either object or ID.
            mode (:obj:`pyosu.GameMode`, optional):
                Game mode category for the score.
                Defaults to pyosu.GameMode.Osu

        Returns:
            pyosu.Score: A score object containing the score on the beatmap.

        """
        bid = beatmap.id if type(beatmap) is Beatmap else beatmap
        connector = self._connector.http
        data = await connector.get_user_beatmap_score(bid, self.id, mode=mode)
        data["score"]["position"] = data["position"]
        return Score(connector=self._connector, data=data["score"])

    async def fetch_kudosu(
        self, *, limit: int = 10, offset: int = 0
    ) -> List[KudosuHistory]:
        """Fetchs user kudosu history. Returns a list with each
        kudosu activity.

        Args:
            limit (:obj:`int`, optional): Limit of items to fetch.
                Defaults to 10.
            offset (:obj:`int`, optional): Offset for pagination.
                Defaults to 0.

        Returns:
            List[pyosu.KudosuHistory]: A list of pyosu.KudosuHistory

        """
        data = await self._connector.http.get_user_kudosu(
            self.id, limit=limit, offset=offset
        )
        return [KudosuHistory(data=d) for d in data]

    async def fetch_scores(
        self,
        type: ScoreType,
        *,
        include_fails: bool = False,
        mode: GameMode = GameMode.Osu,
        limit: int = 10,
        offset: int = 0,
    ) -> List[Score]:
        """Fetchs user recent scores of a given type. Can
        include fails and other game modes.

        Args:
            type (:obj:`pyosu.ScoreType`): A Score type to return.
            include_fails (:obj:`bool`, optional): True to include fails.
                Defaults to False.
            mode (:obj:`pyosu.GameMode`, optional): Scores game mode.
                Defaults to pyosu.GameMode.Osu
            limit (:obj:`int`, optional): Limit of items to fetch.
                Defaults to 10.
            offset (:obj:`int`, optional): Offset for pagination.
                Defaults to 0.

        Returns:
            List[pyosu.Score]: A list containing pyosu.Score objects.

        """
        data = await self._connector.http.get_user_scores(
            self.id,
            type,
            include_fails=include_fails,
            mode=str(mode),
            limit=limit,
            offset=offset,
        )
        return [Score(connector=self._connector, data=d) for d in data]

    async def fetch_beatmaps(
        self,
        *,
        type: BeatmapType = BeatmapType.most_played,
        limit: int = 10,
        offset: int = 0,
    ) -> Union[Beatmapset, BeatmapPlaycount]:
        """Fetchs beatmaps from a user. Returns a list with each
        beatmap or beatmap play counts.

        If the type is pyosu.BeatmapType.most_played it will return
        a list with pyosu.BeatmapPlayCount. Otherwise a list with
        pyosu.Beatmapset.

        Args:
            type (:obj:`pyosu.BeatmapType`, optional): A BeatmapType
                to select. Defaults to pyosu.BeatmapType.most_played
            limit (:obj:`int`, optional): Limit of items to fetch.
                Defaults to 10.
            offset (:obj:`int`, optional): Offset for pagination.
                Defaults to 0.

        Returns:
            Union[Beatmapset, BeatmapPlayCount]: A list that can
                contain either Beatmapset or BeatmapPlayCount objects.
        """
        data = await self._connector.http.get_user_beatmaps(
            self.id, str(type), limit=limit, offset=offset
        )

        if type == BeatmapType.most_played:
            return [
                BeatmapPlaycount(
                    id=d["id"],
                    beatmap=d.get("beatmap"),
                    beatmapset=d.get("beatmapset"),
                    count=d["number"],
                )
                for d in data
            ]
        return [Beatmapset(connector=self._connector, data=d) for d in data]

    async def fetch_activity(
        self, *, limit: int = 10, offset: int = 0
    ) -> List[Event]:
        """Fetchs recent activity from the user.

        Args:
            limit (:obj:`int`, optional): Limit of items to fetch.
                Defaults to 10.
            offset (:obj:`int`, optional): Offset for pagination.
                Defaults to 0.

        Returns:
            List[pyosu.Event]: A list containing pyosu.Event objects.

        """
        data = await self._connector.http.get_user_recent_activity(
            self.id, limit=limit, offset=offset
        )
        return [Event(data=d) for d in data]

    async def create_pm(self, message: str) -> ChatChannel:
        """Creates a private channel to send messages to the user.

        If a PM channel already exists, it will return it from
        cache to avoid repeating the request.

        Note: message parameter acts as a "hello" since it is
        required by the API to give an initial message.

        Args:
            message (:obj:`str`): First message to send

        Returns:
            pyosu.ChatChannel: Chat object that can send and read messages.

        """
        temp = self.pm_channel
        if temp is not None:
            return temp

        data = await self._connector.http.create_new_pm(self.id, message)
        return self._connector.create_pm_channel(self.id, data)
