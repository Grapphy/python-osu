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

from typing import Any, Optional, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .types.rankings import Spotlight as SpotlightPayload
    from .types.rankings import Rankings as RankingsPayload
    from .types.obj import ObjectID


class Spotlight:
    __slots__ = (
        "_connector",
        "id",
        "name",
        "type",
        "start_date",
        "end_date",
        "mode_specific",
        "participant_count",
    )

    if TYPE_CHECKING:
        id: ObjectID
        name: str
        type: str
        start_date: str
        end_date: str
        mode_specific: bool
        participant_count: Optional[int]

    def __init__(
        self, *, connector: Connector, data: SpotlightPayload
    ) -> None:
        self._connector = connector
        self._update_data(data)

    def _update_data(self, data: SpotlightPayload) -> None:
        self.id = data["id"]
        self.name = data["name"]
        self.type = data["type"]
        self.start_date = data["start_date"]
        self.end_date = data["end_date"]
        self.mode_specific = data["mode_specific"]
        self.participant_count = data.get("participant_count")


class Ranking:
    __slots__ = (
        "_connector",
        "beatmapsets",
        "cursor",
        "ranking" "spotlight" "total",
    )

    if TYPE_CHECKING:
        beatmapsets: Optional[List[Dict]]
        cursor: object
        ranking: List[object]
        spotlight: Optional[Spotlight]
        total: int

    def __init__(self, *, connector: Connector, data: RankingsPayload) -> None:
        self._connector = connector
        self._update_data(data)

    def _update_data(self, data: RankingsPayload) -> None:
        self.beatmapsets = data.get("beatmapsets")
        self.cursor = data.get("cursor")
        self.ranking = data["rankings"]
        self.spotlight = data.get("spotlight")
        self.total = data["total"]
