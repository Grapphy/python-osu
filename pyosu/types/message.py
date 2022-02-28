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

from typing import Optional, TypedDict


class ChatMessage(TypedDict):
    message_id: ObjectID
    sender_id: ObjectID
    channel_id: ObjectID
    timestamp: str
    content: str
    is_action: bool
    sender: UserCompact


class CurrentUserAttributes(TypedDict):
    ...


class BeatmapsetDiscussionPermissions(CurrentUserAttributes):
    can_destroy: bool
    can_reopen: bool
    can_moderate_kudosu: bool
    can_resolve: bool
    vote_score: int


class ChatChannelUserAttributes(CurrentUserAttributes):
    can_message: bool
    can_message_error: Optional[str]
    last_read_id: ObjectID


class UserSilence(TypedDict):
    id: ObjectID
    user_id: ObjectID
