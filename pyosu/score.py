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

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .types.score import BaseScore
    from .types.obj import ObjectID


class Score:
    __slots__ = (
        "_connector",
        "id",
        "best_id",
        "user_id",
        "accuracy",
        "mods",
        "score",
        "max_combo",
        "perfect",
        "passed",
        "pp",
        "rank",
        "created_at",
        "mode",
        "mode_int",
        "replay",
        "beatmapset",
        "rank_country",
        "rank_global",
        "weight",
        "user",
        "match",
        "position",
    )

    if TYPE_CHECKING:
        id: ObjectID
        best_id: Optional[ObjectID]
        user_id: ObjectID
        accuracy: int
        mods: Any
        score: Any
        max_combo: Any
        perfect: Any
        passed: bool
        pp: Any
        rank: Any
        created_at: str
        mode: Any
        mode_int: int
        replay: Any
        beatmap: Any
        beatmapset: Optional[Any]
        rank_country: Optional[Any]
        rank_global: Optional[Any]
        weight: Optional[Any]
        user: Optional[Any]
        match: Optional[Any]
        position: Optional[int]

    def __init__(self, *, connector: Connector, data: BaseScore) -> None:
        self._connector = connector
        self._update_data(data)

    def __repr__(self) -> str:
        return (
            f"<Score id={self.id} best_id={self.best_id}"
            f" accuracy={self.accuracy} max_combo={self.max_combo}"
            f" score={self.score}>"
        )

    def __hash__(self) -> int:
        return self.id

    def _update_data(self, data: BaseScore) -> None:
        self.id = data["id"]
        self.best_id = data.get("base_id")
        self.user_id = data["user_id"]
        self.accuracy = data["accuracy"]
        self.mods = data["mods"]
        self.score = data["score"]
        self.max_combo = data["max_combo"]
        self.perfect = data["perfect"]
        self.passed = data["passed"]
        self.pp = data["pp"]
        self.rank = data["rank"]
        self.created_at = data["created_at"]
        self.mode = data["mode"]
        self.mode_int = data["mode_int"]
        self.replay = data["replay"]
        # ! Set from cache or use ID
        # self.beatmap = beatmap
        self.beatmapset = data.get("beatmapset")
        self.rank_country = data.get("rank_country")
        self.rank_global = data.get("rank_global")
        self.weight = data.get("weight")
        self.user = data.get("user")
        self.match = data.get("match")
        self.position = data.get("position")  # If user score
