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

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .types.wiki import WikiPage as WikiPagePayload
    from .connection import Connector


class WikiPage:
    __slots__ = (
        "_connector",
        "layout",
        "locale",
        "markdown",
        "path",
        "tags",
        "title",
        "available_locales",
        "subtitle",
    )

    if TYPE_CHECKING:
        _connector: Connector
        available_locales: List[str]
        layout: str
        locale: str
        markdown: str
        path: str
        subtitle: Optional[str]
        tags: List[str]
        title: str

    def __init__(self, *, connector: Connector, data: WikiPagePayload) -> None:
        self._connector = connector
        self._update_data(data)

    def __repr__(self) -> str:
        return (
            f"<WikiPage title={self.title} tags={self.tags}"
            f" path={self.path} locale={self.locale}"
        )

    def __str__(self) -> str:
        return f"{self.markdown}"

    @property
    def url(self) -> str:
        return f"https://osu.ppy.sh/wiki/{self.locale}/{self.path}"

    def _update_data(self, data: WikiPagePayload) -> None:
        self.layout = data["layout"]
        self.locale = data["locale"]
        self.markdown = data["markdown"]
        self.path = data["path"]
        self.tags = data["tags"]
        self.title = data["title"]
        self.available_locales = data["available_locales"]
        self.subtitle = data.get("subtitle")
