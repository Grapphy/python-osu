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
from .beatmapset import BaseBeatmapset
from .score import Score

from typing import Optional, List, TypedDict, Any


class BaseBeatmap(TypedDict):
    id: ObjectID
    beatmapset_id: ObjectID
    difficulty_rating: float
    mode: str
    status: str
    total_length: int
    user_id: ObjectID
    version: str


class BeatmapCompact(BaseBeatmap, total=False):
    beatmapset: BaseBeatmapset
    checksum: Optional[str]
    failtimes: object
    max_combo: int


class Beatmap(BeatmapCompact, total=False):
    accuracy: float
    ar: float
    beatmapset_id: int
    bpm: Optional[float]
    convert: bool
    count_circles: int
    count_sliders: int
    count_spinners: int
    cs: float
    deleted_at: Optional[str]
    drain: float
    hit_length: int
    is_scoreable: bool
    last_updated: str
    mode_int: int
    passcount: int
    playcount: int
    ranked: int
    url: str


class BeatmapUserScore(TypedDict):
    position: int
    score: Score


class BeatmapScores(TypedDict):
    scores: List[Score]
    userScore: Optional[BeatmapUserScore]
