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


class BaseVersion(TypedDict):
    ...


class BaseBuild(TypedDict):
    id: ObjectID
    created_at: str
    display_version: str
    update_stream: Optional[object]
    users: int
    version: Optional[str]


class Build(BaseBuild, total=False):
    changelog_entries: List[object]
    versions: BaseVersion


class Versions(BaseVersion, total=False):
    next: Optional[BaseVersion]
    previous: Optional[BaseVersion]


class BaseUpdateStream(TypedDict):
    id: ObjectID
    name: str
    display_name: str
    is_featured: bool


class UpdateStream(BaseUpdateStream, total=False):
    latest_build: Optional[Build]
    user_count: int


class BuildList(TypedDict):
    builds: List[Build]
    search_from: Optional[str]
    search_limit: int
    search_max_id: Optional[int]
    search_stream: Optional[str]
    search_to: Optional[str]
    streams: List[UpdateStream]
