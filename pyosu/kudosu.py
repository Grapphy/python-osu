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

from typing import Any, List, Optional, TYPE_CHECKING
from collections import namedtuple


if TYPE_CHECKING:
    from .types.obj import ObjectID
    from .types.kudosu import KudosuHistory as KudosuHistoryPayload


Giver = namedtuple("Giver", "url username")
Post = namedtuple("Post", "title url")


class KudosuHistory:
    __slots__ = (
        "id",
        "action",
        "amount",
        "model",
        "created_at",
        "post",
        "giver",
        "details",
    )

    if TYPE_CHECKING:
        id: ObjectID
        action: str
        amount: int
        model: str
        created_at: str
        giver: Optional[Giver]
        post: Post

    def __init__(self, *, data: KudosuHistoryPayload) -> None:
        self._update_data(data)

    def __repr__(self) -> str:
        return (
            f"<KudosuHistory id={self.id} action={self.action!r}"
            f" model={self.model}"
        )

    def __eq__(self, o: Any) -> bool:
        return isinstance(self, o) and o.id == self.id

    def __ne__(self, o: Any) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        return self.id

    def _update_data(self, data: KudosuHistoryPayload) -> None:
        self.id = data["id"]
        self.action = data["action"]
        self.amount = data["amount"]
        self.model = data["model"]
        self.created_at = data["created_at"]
        self.post = Post(
            title=data["post"]["title"], url=data["post"].get("url")
        )

        try:
            self.giver = Giver(
                url=data["giver"]["url"], username=data["giver"]["username"]
            )
        except (KeyError, TypeError):
            self.giver = None

        self.details = data.get("details")
