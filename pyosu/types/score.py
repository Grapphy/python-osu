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
from typing import Optional, TypedDict, Any


# Not enough documentation
class BaseScore(TypedDict):
    id: ObjectID
    best_id: ObjectID
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


class Score(BaseScore, total=False):
    beatmap: Any
    beatmapset: Any
    rank_country: Any
    rank_global: Any
    weight: Any
    user: Any
    match: Any
