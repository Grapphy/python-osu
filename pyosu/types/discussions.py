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

from typing import Optional, List, TypedDict


class BeatmapsetDiscussionVote(TypedDict):
    id: ObjectID
    user_id: ObjectID
    beatmapset_discussion_id: ObjectID
    created_at: str
    updated_at: str
    score: int


class BeatmapsetDiscussionPost(TypedDict):
    id: ObjectID
    beatmapset_discussion_id: ObjectID
    created_at: str
    deleted_at: Optional[str]
    deleted_by_id: Optional[ObjectID]
    last_editor_id: Optional[ObjectID]
    message: str
    system: bool
    updated_at: str
    user_id: ObjectID


class BeatmapsetDiscussion(TypedDict):
    id: ObjectID
    beatmap: object
    beatmap_id: Optional[ObjectID]
    beatmapset: object
    beatmapset_id: int
    can_be_resolved: bool
    can_grant_kudosu: bool
    created_at: str
    current_user_attributes: object
    deleted_at: str
    deleted_by_id: Optional[ObjectID]
    kudosu_denied: bool
    last_post_at: str
    message_type: object
    parent_id: Optional[ObjectID]
    posts: Optional[List[BeatmapsetDiscussionPost]]
    resolved: bool
    starting_post: Optional[BeatmapsetDiscussionPost]
    timestamp: Optional[str]
    updated_at: str
    user_id: ObjectID


class BeatmapsetDiscussionPostList(TypedDict):
    beatmapsets: object
    cursor: object
    posts: List[BeatmapsetDiscussionPost]
    users: List[UserCompact]


class BeatmapsetDiscussionVoteList(TypedDict):
    cursor: object
    discussions: List[BeatmapsetDiscussion]
    users: List[UserCompact]
    votes: List[BeatmapsetDiscussionVote]


class BeatmapsetDiscussionList(TypedDict):
    beatmaps: object
    cursor: object
    discussions: List[BeatmapsetDiscussion]
    included_discussions: List[BeatmapsetDiscussion]
    reviews_config_max_blocks: int
    users: List[UserCompact]
