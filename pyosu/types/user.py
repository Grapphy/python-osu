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
from typing import Optional, List, TypedDict


class UserCompact(TypedDict):
    id: ObjectID
    username: str
    avatar_url: str
    country_code: str
    default_group: str
    last_visit: Optional[str]
    profile_colour: Optional[str]
    is_active: bool
    is_bot: bool
    is_deleted: bool
    is_online: bool
    is_supporter: bool
    pm_friends_only: bool


class User(UserCompact, total=False):
    cover_url: str
    has_supported: bool
    join_date: str
    kudosu_available: int
    kudosu_total: int
    max_blocks: int
    max_friends: int
    post_count: int
    playmode: object
    playstyle: List[str]
    profile_order: List[object]
    title: Optional[str]
    title_url: Optional[str]
    discord: Optional[str]
    twitter: Optional[str]
    website: Optional[str]
    location: Optional[str]
    interests: Optional[str]
    occupation: Optional[str]
