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

import asyncio
import aiohttp

from .http import HTTPClient
from .user import User
from .connection import Connector
from .beatmap import Beatmap
from .beatmapset import Beatmapset
from .forum import ForumTopic, ForumPoll
from .wiki import WikiPage
from .rankings import Spotlight, Ranking
from .news import NewsPostList
from .build import BuildChangelog

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .enums import ChangelogStream
    from .types.obj import ObjectID


class Client:
    def __init__(
        self,
        *,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        **config: Any,
    ) -> None:
        self.loop: asyncio.AbstractEventLoop = (
            loop if loop else asyncio.new_event_loop()
        )

        ssl: Optional[bool] = config.pop("ssl", False)
        proxy: Optional[str] = config.pop("proxy", None)
        proxy_auth: Optional[aiohttp.BasicAuth] = config.pop(
            "proxy_auth", None
        )

        self.http: HTTPClient = HTTPClient(
            proxy=proxy, proxy_auth=proxy_auth, ssl=ssl
        )
        self._connection: Connector = self._get_connection()

    def _get_connection(self) -> Connector:
        return Connector(http=self.http)

    @property
    def user(self) -> Optional[User]:
        return self._connection.user

    async def login(self, username: str, password: str) -> None:
        """Creates OAuth token for all scopes using username
        and password. This allows the client to use lazer
        and resource owner endpoints.

        Args:
            username (:obj:`str`): Account username.
            password (:obj:`str`): Account password.
        """
        await self.http.oauth_login(
            grant_type="password",
            scope="*",
            username=username,
            password=password,
        )

        data = await self.http.get_own_user()
        self._connection.user = User(connector=self._connection, data=data)

    async def oauth_login(self, client_id: int, client_secret: str) -> None:
        """Creates OAuth token for public scopes using a given client ID
        and client secret. This allows just a small number of endpoints.

        Args:
            client_id (:obj:`int`): Client ID number.
            client_secret (:obj:`str`): Client secret string.
        """
        await self.http.oauth_login(
            grant_type="client_credentials",
            scope="public",
            client_id=client_id,
            client_secret=client_secret,
        )

    async def public_login(self) -> None:
        """Creates OAuth token for public scopes using the default client ID
        and client secret that is used in-game. (Which I assume it is okay
        to use).
        """
        await self.http.oauth_login(
            grant_type="client_credentials", scope="public"
        )

    async def fetch_beatmapset(self, beatmapset_id: int, /) -> Beatmapset:
        data = await self.http.get_beatmapset(beatmapset_id)
        return Beatmapset(connector=self._connection, data=data)

    async def fetch_beatmap(self, beatmap_id: int, /) -> Beatmap:
        """Fetchs a beatmap by ID.

        Args:
            beatmap_id (:obj:`int`): beatmap id

        Returns:
            :obj:`pyosu.Beatmap`
        """
        data = await self.http.get_beatmap(beatmap_id)
        return Beatmap(connector=self._connection, data=data)

    async def fetch_build_changelog(
        self, stream: ChangelogStream, build: str
    ) -> BuildChangelog:
        """Returns changelog from a build. You need to provide the
        stream where the build is referenced.

        Args:
            stream (:obj:`pyosu.ChangelogStream`): Valid osu stream.
            build (:obj:`str`): Build version.

        Returns:
            :obj:`pyosu.BuildChangelog`
        """
        data = await self.http.get_changelog_build(str(stream), build)
        return BuildChangelog(data=data)

    async def fetch_changelog(
        self, query: Union[ObjectID, ChangelogStream], by_id: bool = False
    ) -> BuildChangelog:
        """Returns recent changelog from a stream or changelog from a given
        build. by_id must be true if you're giving a build ID instead of
        build name.

        Args:
            query (:obj: `pyosu.ChangelogStream`): A stream or build version.
            by_id (:obj: `bool`): True if you want to search a build ID rather
            than by build name.

        Returns:
            :obj:`pyosu.BuildChangelog`
        """
        key = "id" if by_id else None
        data = await self.http.lookup_changelog_build(str(query), key=key)
        return BuildChangelog(data=data)

    async def fetch_topic(self, topic_id: ObjectID, /) -> ForumTopic:
        data = await self.http.get_topic_with_posts(topic_id)
        return ForumTopic(connector=self._connection, data=data)

    async def create_topic(
        self,
        forum_id: ObjectID,
        title: str,
        body: str,
        *,
        poll: ForumPoll = None,
    ) -> ForumTopic:
        kwargs: Dict[str, Any] = {"with_poll": False}

        if poll is not None:
            kwargs["with_poll"] = True
            kwargs["p_hide_results"] = poll.hide_results
            kwargs["p_length_days"] = poll.length_days
            kwargs["p_max_options"] = poll.max_options
            kwargs["p_options"] = poll.options_as_string
            kwargs["p_title"] = poll.title
            kwargs["p_vote_change"] = poll.vote_change

        data = await self.http.create_topic(body, forum_id, title, **kwargs)
        return ForumTopic(connector=self._connection, data=data)

    async def fetch_news(self, limit: int = 10, /) -> NewsPostList:
        """Fetchs news from osu.
        Args:
            limit (:obj:`int`): items limit

        Returns:
            :obj:`pyosu.NewsPostList`
        """
        data = await self.http.get_news_listing(limit=limit)
        return NewsPostList(connector=self._connection, data=data)

    async def fetch_ranking(
        self, mode: str = "osu", type: str = "score", /
    ) -> Ranking:
        """Fetchs rankings from osu.

        Args:
            mode (:obj:`str`): osu gamemode
            type (:obj:`str`): ranking type

        Returns:
            :obj:`pyosu.Ranking`
        """
        data = await self.http.get_rankings(mode=mode, type=type)
        return Ranking(connector=self._connection, data=data)

    async def fetch_spotlights(self) -> List[Spotlight]:
        """Fetchs spotlights from page.

        Returns:
            :obj:`list[pyosu.Beatmap]`
        """
        data = await self.http.get_spotlights()
        return [
            Spotlight(connector=self._connection, data=d)
            for d in data["spotlights"]
        ]

    async def fetch_user(self, user_id: int, /) -> User:
        """Fetchs information from a user.

        Args:
            user_id (:obj:`int`): user id

        Returns:
            :obj:`pyosu.User`
        """
        data = await self.http.get_user(user_id)
        return User(connector=self._connection, data=data)

    async def fetch_users_bulk(self, users_id: List[int], /) -> List[User]:
        """Fetchs a list of users.

        Args:
            users_id (:obj:`list`): List containing users id to fetch

        Returns:
            List[pyosu.User]: Returns a list with pyosu.User objects

        """
        data = await self.http.get_users(users_id)
        return [User(connector=self._connection, data=d) for d in data]

    async def fetch_wiki(
        self, locale: str = "en", path: str = "Welcome"
    ) -> WikiPage:
        """Fetchs a wiki page.

        Args:
            locale (:obj:`str`): locale to query from wiki
            path (:obj:`str`): page to query form wiki

        Returns:
            :obj:`pyosu.Wikipage`
        """
        data = await self.http.get_wiki_page(locale=locale, path=path)
        return WikiPage(connector=self._connection, data=data)

    async def logout(self) -> None:
        """Closes the connection and deletes token"""
        await self.http.delete_current_token()
        await self.http.close_session()
