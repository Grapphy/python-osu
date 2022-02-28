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
from typing import Optional, List, TypedDict, Any


class CommentableMeta(TypedDict):
    id: ObjectID
    title: str
    type: str
    url: str


class Comment(TypedDict):
    id: ObjectID
    commentable_id: ObjectID
    commentable_type: str
    created_at: str
    deleted_at: Optional[str]
    edited_at: Optional[str]
    edited_by_id: Optional[ObjectID]
    legacy_name: Optional[str]
    message: Optional[str]
    message_html: Optional[str]
    parent_id: Optional[ObjectID]
    pinned: bool
    replies_count: int
    updated_at: str
    user_id: ObjectID
    votes_count: int


class CommentBundle(TypedDict):
    commentable_meta: List[CommentableMeta]
    comments: List[Comment]
    cursor: object
    has_more: bool
    has_more_id: Optional[ObjectID]
    included_comments: List[Comment]
    pinned_comments: Optional[List[Comment]]
    sort: str
    top_level_count: Optional[int]
    total: Optional[int]
    user_follow: bool
    user_votes: List[int]
    users: List[UserCompact]
