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

from collections import namedtuple

from .score import Score
from .enums import GameMode, RankingType

if TYPE_CHECKING:
    from .connection import Connector
    from .types.beatmap import Beatmap as BeatmapPayload
    from .types.beatmap import BeatmapScores as BeatmapScoresPayload


BeatmapPlaycount = namedtuple(
    "BeatmapPlaycount", "id beatmap beatmapset count"
)


class BeatmapScores:
    def __init__(
        self,
        *,
        connector: Connector,
        data: BeatmapScoresPayload,
        beatmap: Beatmap,
    ) -> None:
        self._connector = connector
        self.beatmap = beatmap
        self._update_data(data)

    def _update_data(self, data: BeatmapScoresPayload) -> None:
        self.scores = [
            Score(connector=self._connector, data=d) for d in data["scores"]
        ]

        self.user_score = data.get("userScore")


class BaseBeatmap:
    def __init__(self, *, connector: Connector, data: BeatmapPayload) -> None:
        self._connector = connector
        self._update_data(data)

    def __repr__(self) -> str:
        return (
            f"<Beatmap id={self.id} mode={self.mode}"
            f" status={self.status} version={self.version}"
            f" difficulty={self.difficulty_rating}>"
        )

    def __eq__(self, o: Any) -> bool:
        return isinstance(self, o) and o.id == self.id

    def __ne__(self, o: Any) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        return self.id

    def _update_data(self, data: BeatmapPayload) -> None:
        self.id = data["id"]
        self.mode = data["mode"]
        self.status = data["status"]
        self.total_length = data["total_length"]
        self.user_id = data["user_id"]
        self.version = data["version"]
        self.beatmapset_id = data["beatmapset_id"]
        self.difficulty_rating = data["difficulty_rating"]
        # requires handling
        self.beatmapset = data.get("beatmapset")
        self.checksum = data.get("checksum")
        self.failtimes = data.get("failtimes")
        self.max_combo = data.get("max_combo")
        self.accuracy = data.get("accuracy")
        self.ar = data.get("ar")
        self.bpm = data.get("bpm")
        self.convert = data.get("convert")
        self.count_circles = data.get("count_circles")
        self.count_sliders = data.get("count_sliders")
        self.count_spinners = data.get("count_spinners")
        self.cs = data.get("cs")
        self.deleted_at = data.get("deleted_at")
        self.drain = data.get("drain")
        self.hit_length = data.get("hit_length")
        self.is_scoreable = data.get("is_scoreable")
        self.last_update = data.get("last_update")
        self.mode_int = data.get("mode_int")
        self.passcount = data.get("passcount")
        self.playcount = data.get("playcount")
        self.ranked = data.get("ranked")
        self.url = data.get("url")


class Beatmap(BaseBeatmap):
    def __init__(self, *, connector: Connector, data: BeatmapPayload) -> None:
        super().__init__(connector=connector, data=data)

    @property
    def scores(self) -> BeatmapScores:
        return self._connector._get_cached_beatmapscore(self.id)

    async def fetch_scores(
        self,
        *,
        mode: Optional[GameMode] = GameMode.Osu,
        type: Optional[RankingType] = None,
    ) -> BeatmapScores:
        temp = self.scores
        if temp is not None:
            return temp

        data = await self._connector.http.get_beatmap_scores(
            self.id, mode=mode, type=type
        )
        return self._connector.create_beatmapscore(self, data)
