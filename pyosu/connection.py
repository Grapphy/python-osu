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

from typing import Any, Dict, TYPE_CHECKING

from collections import OrderedDict

from .channel import ChatChannel
from .beatmap import BeatmapScores
from .user import User
from .beatmap import Beatmap

if TYPE_CHECKING:
    from .types.user import User as UserPayload
    from .types.beatmap import Beatmap as BeatmapPayload
    from .http import HTTPClient
    from .channel import ChatChannel


class Connector:
    def __init__(self, http: HTTPClient) -> None:
        self.http: HTTPClient = http
        self.init_values()

    def init_values(self) -> None:
        self.user: Optional[User] = None
        self.users: Dict[int, User] = {}
        self.beatmaps: Dict[int, Beatmap] = {}
        self.pm_channels: OrderedDict[int, ChatChannel] = OrderedDict()
        self.beatmapscores: OrderedDict[int, BeatmapScores] = OrderedDict()

    def _get_cached_pmchannel(self, user_id: int) -> ChatChannel:
        return self.pm_channels.get(user_id)

    def _get_cached_beatmapscore(self, beatmap_id: int) -> BeatmapScores:
        return self.beatmapscores.get(beatmap_id)

    def _add_user_cache(self, data: UserPayload) -> User:
        try:
            return self.users[int(data["id"])]
        except KeyError:
            user = User(connector=self, data=data)
            self.users[user.id] = user
            return user

    def _add_beatmap_cache(self, data: BeatmapPayload) -> Beatmap:
        try:
            return self.beatmaps[int(data["id"])]
        except KeyError:
            beatmap = Beatmap(connector=self, data=data)
            self.beatmaps[beatmap.id] = beatmap
            return beatmap

    def _add_pm_channel_cache(
        self, user_id: int, channel: ChatChannel
    ) -> None:
        self.pm_channels[user_id] = channel

        if len(self.pm_channels) > 64:
            self.pm_channels.popitem(last=False)

    def _add_beatmapscores_cache(
        self, beatmap_id: int, beatmapscore: BeatmapScores
    ) -> None:
        self.beatmapscores[beatmap_id] = beatmapscore

        if len(self.beatmapscores) > 64:
            self.beatmapscores.popitem(last=False)

    def create_pm_channel(self, user_id: int, data: object) -> ChatChannel:
        channel_data = data.get("channel") or data

        pm_channel = ChatChannel(connector=self, data=channel_data)
        if user_id not in self.pm_channels:
            self._add_pm_channel_cache(user_id, pm_channel)

        return pm_channel

    def create_beatmapscore(
        self, beatmap: Beatmap, data: object
    ) -> BeatmapScores:
        beatmapscore = BeatmapScores(
            connector=self, data=data, beatmap=beatmap
        )
        if beatmap.id not in self.beatmapscores:
            self._add_beatmapscores_cache(beatmap.id, beatmapscore)

        return beatmapscore

    async def _get_presence(self) -> None:
        data = await self.http.get_presence()

        for channel in data:
            if channel["type"] == "PM":
                author = [i for i in channel["users"] if i != self.user.id][0]
                self.create_pm_channel(author, channel)

        data = await self.http.get_users(self.pm_channels.keys())
        [self._add_user_cache(user) for user in data["users"]]
