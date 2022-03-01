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

from typing import Any, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .types.user import User as UserPayload
    from .types.beatmapset import Beatmapset as BeatmapsetPayload
    from .connection import Connector


class BaseBeatmapset:
    def __init__(
        self, *, connector: Connector, data: BeatmapsetPayload
    ) -> None:
        self._connector = connector
        self._update_data(data)

    def __repr__(self) -> str:
        return (
            f"<Beatmapset id={self.id} artist={self.artist}"
            f" creator={self.creator} play_count={self.play_count}"
            f" nsfw={self.nsfw}> title={self.title!r}"
        )

    def __str__(self) -> str:
        return self.title

    def __eq__(self, o: Any) -> bool:
        return isinstance(self, o) and o.id == self.id

    def __ne__(self, o: Any) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        return self.id

    def _update_data(self, data: BeatmapsetPayload) -> None:
        self.id = data["id"]
        self.artist = data["artist"]
        self.artist_unicode = data["artist_unicode"]
        self.covers = data["covers"]
        self.creator = data["creator"]
        self.favourite_count = data["favourite_count"]
        self.nsfw = data["nsfw"]
        self.play_count = data["play_count"]
        self.preview_url = data["preview_url"]
        self.source = data["source"]
        self.status = data["status"]
        self.title = data["title"]
        self.title_unicode = data["title_unicode"]
        self.user_id = data["user_id"]
        self.video = data["video"]
        self.converts = data.get("converts")
        self.current_user_attributes = data.get("current_user_attributes")
        self.description = data.get("description")
        self.discussions = data.get("discussions")
        self.events = data.get("events")
        self.genre = data.get("genre")
        self.has_favourited = data.get("has_favourited")
        self.language = data.get("language")
        self.nominations = data.get("nominations")
        self.ratings = data.get("ratings")
        self.recent_favourites = data.get("recent_favourites")
        self.related_users = data.get("related_users")
        self.download_disabled = data.get("download_disabled")
        self.more_information = data.get("more_information")
        self.bpm = data.get("bpm")
        self.can_be_hyped = data.get("can_be_hyped")
        self.creator = data.get("creator")
        self.discussion_enabled = data.get("discussion_enabled")
        self.discussion_locked = data.get("discussion_locked")
        self.hype_current = data.get("hype_current")
        self.hype_required = data.get("hype_required")
        self.is_scoreable = data.get("is_scoreable")
        self.last_updated = data.get("last_updated")
        self.legacy_thread_url = data.get("legacy_thread_url")
        self.nominations_current = data.get("nominations_current")
        self.nominations_required = data.get("nominations_required")
        self.ranked = data.get("ranked")
        self.ranked_date = data.get("ranked_date")
        self.source = data.get("source")
        self.storyboard = data.get("storyboard")
        self.submitted_date = data.get("submitted_date")
        self.tags = data.get("tags")

        for handler in ("user", "beatmaps"):
            try:
                getattr(self, f"_handle_{handler}")(data[handler])
            except KeyError:
                continue

    def _handle_user(self, data: UserPayload) -> None:
        self.user = self._connector._add_user_cache(data)

    def _handle_beatmaps(self, data: BeatmapPayload) -> None:
        self.beatmaps = [
            self._connector._add_beatmap_cache(beatmap) for beatmap in data
        ]


class Beatmapset(BaseBeatmapset):
    def __init__(
        self, *, connector: Connector, data: BeatmapsetPayload
    ) -> None:
        super().__init__(connector=connector, data=data)
