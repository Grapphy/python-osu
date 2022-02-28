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

from .obj import ObjectID
from typing import Optional, List, TypedDict, Any


class BaseBeatmapset(TypedDict):
    id: ObjectID
    artist: str
    artist_unicode: str
    covers: object
    creator: str
    favourite_count: str
    nsfw: bool
    play_count: int
    preview_url: str
    source: str
    status: str
    title: str
    title_unicode: str
    user_id: ObjectID
    video: bool


class BeatmapsetCompact(BaseBeatmapset, total=False):
    beatmaps: Optional[List[Beatmap]]
    converts: Optional[Any]
    current_user_attributes: Optional[Any]
    description: Optional[Any]
    discussions: Optional[Any]
    events: Optional[Any]
    genre: Optional[Any]
    has_favourited: Optional[bool]
    language: Optional[Any]
    nominations: Optional[Any]
    ratings: Optional[Any]
    recent_favourites: Optional[Any]
    related_users: Optional[Any]
    user: Optional[Any]


class Beatmapset(BeatmapsetCompact, total=False):
    download_disabled: bool
    more_information: Optional[str]
    bpm: float
    can_be_hyped: bool
    creator: str
    discussion_enabled: bool
    discussion_locked: bool
    hype_current: int
    hype_required: int
    is_scoreable: bool
    last_updated: str
    legacy_thread_url: Optional[str]
    nominations_current: int
    nominations_required: int
    ranked: int
    ranked_date: Optional[str]
    source: str
    storyboard: bool
    submitted_date: Optional[str]
    tags: str
    has_favourited: bool
