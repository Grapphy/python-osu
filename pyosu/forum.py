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

from typing import Any, Optional, AsyncIterator, TYPE_CHECKING

if TYPE_CHECKING:
    from .types.obj import ObjectID
    from .connection import Connector
    from .types.forum import ForumNavigation as ForumNavigationPayload
    from .types.forum import ForumPost as ForumPostPayload


class ForumPost:
    def __init__(
        self, *, connector: Connector, data: ForumPostPayload
    ) -> None:
        self._connector = connector
        self._update_data(data)

    def _update_data(self, data: ForumPostPayload) -> None:
        self.id = data["id"]
        self.topic_id = data["topic_id"]  # Point to ForumTopic obj
        self.user_id = data["user_id"]  # Point to User obj
        self.created_at = data["created_at"]
        self.deleted_at = data.get("deleted_at")
        self.edited_at = data.get("edited_at")
        self.edited_by_id = data.get("edited_by_id")
        self.forum_id = data.get("forum_id")
        self.html = data["body"].get("html")
        self.raw = data["body"].get("raw")


class ForumTopic:
    def __init__(
        self, *, connector: Connector, data: ForumNavigationPayload
    ) -> None:
        self._connector = connector
        self._update_data(data)

    def __repr__(self) -> str:
        return (
            f"<ForumTopic id={self.id} title={self.title!r}"
            f" last_post={self.updated_at} locked={self.is_locked}>"
        )

    def _update_data(self, data: ForumNavigationPayload) -> None:
        self._search = data["search"]
        self.posts = data["posts"]

        self.id = data["topic"]["id"]
        self.created_at = data["topic"]["id"]
        self.deleted_at = data["topic"].get("deleted_at")
        self.first_post_id = data["topic"]["first_post_id"]
        self.forum_id = data["topic"]["forum_id"]
        self.is_locked = data["topic"]["is_locked"]
        self.last_post_id = data["topic"]["last_post_id"]
        self.post_count = data["topic"]["post_count"]
        self.title = data["topic"]["title"]
        self.type = data["topic"]["type"]
        self.updated_at = data["topic"]["updated_at"]
        self.user_id = data["topic"]["user_id"]

        self._cursor_string = ""

    async def fetch_posts(
        self, *, limit: int = 50
    ) -> AsyncIterator[ForumPost]:
        while True:
            _limit = min(50 if limit is None else limit, 50)
            if _limit < 1:
                return

            data = await self._connector.http.get_topic_with_posts(
                self.id, cursor=self._cursor_string, limit=_limit
            )

            self._cursor_string = data["cursor_string"]

            if not data["posts"]:
                return

            for post in data["posts"]:
                yield ForumPost(connector=self._connector, data=post)

            if not self._cursor_string:
                return
