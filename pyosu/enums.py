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

from enum import Enum


class ChangelogStream:
    Stable40 = "stable40"
    Stable = "stable"
    Beta40 = "beta40"
    CuttingEdge = "cuttingedge"
    Lazer = "lazer"
    Web = "web"


class GameMode:
    Fruits = "fruits"
    Mania = "mania"
    Osu = "osu"
    Taiko = "taiko"


class RankingType:
    Charts = "charts"
    Country = "country"
    Performance = "performance"
    Score = "score"


class ScoreType(Enum):
    best = 0
    firsts = 1
    recent = 2

    def __str__(self):
        return self.name


class BeatmapType(Enum):
    favourite = 0
    graveyard = 1
    loved = 2
    most_played = 3
    pending = 4
    ranked = 5

    def __str__(self):
        return self.name
