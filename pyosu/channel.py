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

from typing import Any, Dict, Optional, List, TYPE_CHECKING
from .message import ChatMessage

if TYPE_CHECKING:
    from .http import HTTPClient
    from .connection import Connector
    from .types.obj import ObjectID
    from .types.message import CurrentUserAttributes, ChatMessage


class ChatChannel:
    __slots__ = (
        "id",
        "current_user_attributes",
        "_connector",
        "name",
        "description",
        "icon",
        "type",
        "last_read_id",
        "last_message_id",
        "recent_messages",
        "moderated",
        "users",
    )

    if TYPE_CHECKING:
        channel_id: ObjectID
        _connector: Connector
        name: str
        icon: str
        type: str
        moderated: bool
        last_read_id: Optional[ObjectID]
        last_message_id: Optional[ObjectID]
        recent_messages: Optional[List[ChatMessage]]
        description: Optional[str]
        users: Optional[List[ObjectID]]
        current_user_attributes: Optional[CurrentUserAttributes]

    def __init__(self, *, connector: Connector, data: object) -> None:
        self._connector = connector
        self._update_data(data)

    def __str__(self) -> str:
        return f"channel={self.id} name={self.name} type={self.type}"

    def _update_data(self, data: object) -> None:
        self.id = int(data["channel_id"])
        self.name = data["name"]
        self.icon = data["icon"]
        self.type = data["type"]
        self.moderated = data["moderated"]
        self.last_read_id = data.get("last_read_id", 0)
        self.last_message_id = data.get("last_message_id", 0)
        self.recent_messages = data.get("recent_messages", [])
        self.users = data.get("users", [])

    async def mark_as_read(self) -> None:
        await self._connector.http.mark_channel_as_read(
            self.id,
            self.last_message_id,
            channel_id=self.id,
            message_id=self.last_message_id,
        )

    async def send(self, message: str) -> ChatMessage:
        data = await self._connector.http.send_message_to_channel(
            self.id, message
        )
        return ChatMessage(connector=self._connector, data=data)
