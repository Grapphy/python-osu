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
from .user import UserCompact
from .message import ChatMessage, CurrentUserAttributes, UserSilence

from typing import Optional, List, TypedDict, Any


class ChatChannel(TypedDict):
    channel_id: ObjectID
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


class NewChannel(TypedDict):
    new_channel_id: ObjectID
    presence: ChatChannel
    message: ChatMessage


class ChannelUpdate(TypedDict):
    messages: Optional[List[ChatMessage]]
    presence: Optional[List[ChatChannel]]
    silences: Optional[List[UserSilence]]


class DetailedChannel(TypedDict):
    channel: ChatChannel
    users: List[UserCompact]
