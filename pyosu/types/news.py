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


class BaseNewsPost(TypedDict):
    id: ObjectID
    author: str
    edit_url: str
    first_img: Optional[str]
    published_at: str
    slug: str
    title: str
    updated_at: str


class Navigation(TypedDict):
    newer: Optional[BaseNewsPost]
    older: Optional[BaseNewsPost]


class NewsPost(BaseNewsPost, total=False):
    content: str
    navigation: Navigation
    preview: str


class NewsPostList(TypedDict):
    cursor: object
    news_posts: List[NewsPost]
    current_year: int
    year_news_posts: List[NewsPost]
    year_listing: List[int]
    search_limit: int
    search_sort: str
