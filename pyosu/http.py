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
from typing import (
    Any,
    ClassVar,
    Union,
    Optional,
    Dict,
    TYPE_CHECKING,
    Coroutine,
    TypeVar,
    List,
)

import aiohttp
import asyncio
import json

from .oauth import OAuth

if TYPE_CHECKING:
    from .types import (
        beatmap,
        beatmapset,
        build,
        channel,
        message,
        forum,
        comment,
        user,
        kudosu,
        event,
        score,
        beatmap,
        rankings,
        news,
        discussions,
        wiki,
        multiplayer,
        notifications,
    )
    from .types.obj import ObjectID

    T = TypeVar("T")
    Response = Coroutine[Any, Any, T]


class Route:
    BASE: ClassVar[str] = "https://osu.ppy.sh/api/v2"

    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.method: str = method
        self.path: str = path
        self.url: str = self.BASE + self.path

        if parameters:
            self.url = self.url.format_map(parameters)


class HTTPClient:
    def __init__(
        self,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        ssl: Optional[bool] = True,
    ) -> None:
        self.__session: aiohttp.ClientSession = None
        self.proxy: Optional[str] = proxy
        self.proxy_auth: Optional[aiohttp.BasicAuth] = proxy_auth
        self.ssl: bool = ssl
        self.user_agent: str = "osu!"
        self.token: str = None

    async def request(self, route: Route, **kwargs: Any) -> Any:
        url = route.url
        method = route.method
        headers: Dict[str, str] = {
            "User-Agent": self.user_agent,
            "Authorization": f"Bearer {self.token}",
        }

        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = json.dumps(kwargs.pop("json"))

        kwargs["headers"] = headers

        if self.proxy is not None:
            kwargs["proxy"] = self.proxy
        if self.proxy_auth is not None:
            kwargs["proxy_auth"] = self.proxy_auth

        async with self.__session.request(method, url, **kwargs) as res:
            if res.headers["content-type"] == "application/json":
                response = await res.json()
            else:
                response = await res.text()

            if res.status == 404:
                raise Exception("Not found", response)

            if res.status == 401:
                raise Exception("Unauthorized", response)

        return response

    def reopen_session(self) -> None:
        if self.__session.closed:
            self.__session = aiohttp.ClientSession()

    async def oauth_login(
        self,
        grant_type: Optional[str] = None,
        scope: Optional[str] = None,
        **parameters,
    ) -> None:
        self.__session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=self.ssl)
        )
        oauth = OAuth(grant_type, scope, **parameters)
        res = await oauth.authenticate(
            self.__session,
            proxy=self.proxy,
            proxy_auth=self.proxy_auth,
            user_agent=self.user_agent,
        )

        if "error" in res:
            raise Exception(res["error"], res["message"])

        self.token = res.get("access_token")

    async def close_session(self) -> None:
        if self.__session:
            await self.__session.close()

    ########################### Beatmaps

    def lookup_beatmap(
        self,
        map_id: ObjectID,
        checksum: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> Response[beatmap.Beatmap]:
        params: Dict[str, Any] = {"id": map_id}

        if checksum:
            params["checksum"] = checksum
        if filename:
            params["filename"] = filename

        return self.request(Route("GET", "/beatmaps/lookup"), params=params)

    def get_user_beatmap_score(
        self,
        beatmap_id: ObjectID,
        user_id: ObjectID,
        mode: str = "osu",
        mods: str = None,
    ) -> Response[beatmap.BeatmapUserScore]:
        r = Route(
            "GET",
            "/beatmaps/{beatmap}/scores/users/{user}",
            beatmap=beatmap_id,
            user=user_id,
        )
        params: Dict[str, Any] = {"mode": mode}

        if mods:
            params["mods"] = mods

        return self.request(r, params=params)

    def get_beatmap_scores(
        self,
        beatmap_id: ObjectID,
        mode: str = "osu",
        mods: str = None,
        type: str = None,
    ) -> Response[beatmap.BeatmapScores]:
        params: Dict[str, Any] = {"mode": mode}

        if mods:
            params["mods"] = mods

        if type:
            params["type"] = type

        return self.request(
            Route("GET", "/beatmaps/{beatmap}/scores", beatmap=beatmap_id),
            params=params,
        )

    def get_beatmaps(
        self, beatmaps: List[ObjectID]
    ) -> Response[List[beatmap.Beatmap]]:
        params = "&".join([f"ids[]={str(x)}" for x in beatmaps])
        path = f"/beatmaps?{params}"

        return self.request(Route("GET", path))

    def get_beatmap(self, beatmap_id: ObjectID) -> Response[beatmap.Beatmap]:
        return self.request(
            Route("GET", "/beatmaps/{beatmap}", beatmap=beatmap_id)
        )

    ########################### Beatmapsets

    def get_beatmapset(
        self, beatmapset_id: ObjectID
    ) -> Response[beatmapset.Beatmapset]:
        return self.request(
            Route("GET", "/beatmapsets/{bmapset}", bmapset=beatmapset_id)
        )

    def search_beatmap(self, query: str) -> Response:
        params: Dict[str, str] = {"q": query}

        return self.request(Route("GET", "/beatmapsets/search"), params=params)

    ########################### Beatmapset Discussions

    def get_beatmapset_discussion_posts(
        self,
        discussion_id: ObjectID = None,
        limit: int = 10,
        page: int = 0,
        sort: str = "id_desc",
        types: str = "reply",
        user_id: ObjectID = None,
        with_deleted: str = None,
    ) -> Response[discussions.BeatmapsetDiscussionPostList]:
        params: Dict[str, Any] = {
            "limit": limit,
            "page": page,
            "sort": sort,
            "types[]": types,
        }

        if discussion_id:
            params["beatmapset_discussion_id"] = discussion_id

        if user_id:
            params["user"] = user_id

        if with_deleted:
            params["with_deleted"] = with_deleted

        return self.request(
            Route("GET", "/beatmapsets/discussions/posts"), params=params
        )

    def get_beatmapset_discussion_votes(
        self,
        discussion_id: ObjectID = None,
        limit: int = 10,
        page: int = 0,
        receiver: ObjectID = None,
        score: str = "1",
        sort: str = "id_desc",
        user_id: ObjectID = None,
        with_deleted: str = None,
    ) -> Response[discussions.BeatmapsetDiscussionVoteList]:
        params: Dict[str, Any] = {
            "limit": limit,
            "page": page,
            "score": score,
            "sort": sort,
        }

        if discussion_id:
            params["beatmapset_discussion_id"] = discussion_id

        if receiver:
            params["receiver"] = receiver

        if user_id:
            params["user"] = user_id

        if with_deleted:
            params["with_deleted"] = with_deleted

        return self.request(
            Route("GET", "/beatmapsets/discussions/votes"), params=params
        )

    def get_beatmapset_discussions(
        self,
        beatmap_id: ObjectID = None,
        beatmapset_id: ObjectID = None,
        beatmapset_status: str = "all",
        limit: int = 10,
        message_types: str = None,
        only_unresolved: bool = False,
        page: int = 0,
        sort: str = "id_desc",
        user_id: ObjectID = None,
        with_deleted: str = None,
    ) -> Response[discussions.BeatmapsetDiscussionList]:
        params: Dict[str, Any] = {
            "beatmapset_status": beatmapset_status,
            "limit": limit,
            "only_unresolved": only_unresolved,
            "page": page,
            "sort": sort,
        }

        if beatmap_id:
            params["beatmap_id"] = beatmap_id

        if beatmapset_id:
            params["beatmapset_id"] = beatmapset_id

        if message_types:
            params["message_types[]"] = message_types

        if user_id:
            params["user"] = user_id

        if with_deleted:
            params["with_deleted"] = with_deleted

        return self.request(
            Route("GET", "/beatmapsets/discussions"), params=params
        )

    ########################### Changelog

    def get_changelog_build(
        self, stream: str, build: str
    ) -> Response[build.Build]:
        return self.request(
            Route(
                "GET",
                "/changelog/{stream}/{build}",
                stream=stream,
                build=build,
            )
        )

    def get_changelog_listing(
        self,
        from_build: str = None,
        max_id: ObjectID = None,
        stream: str = None,
        to_build: str = None,
        message_format: str = "html",
    ) -> Response[build.BuildList]:
        params: Dict[str, Any] = {"message_formats[]": message_format}

        if from_build:
            params["from"] = from_build

        if max_id:
            params["max_id"] = max_id

        if stream:
            params["stream"] = stream

        if to_build:
            params["to"] = to_build

        return self.request(Route("GET", "/changelog"), params=params)

    def lookup_changelog_build(
        self, changelog: str, key: str = None, message_format: str = "html"
    ) -> Response[build.Build]:
        params: Dict[str, Any] = {"message_formats[]": message_format}

        if key:
            params["key"] = key

        return self.request(
            Route("GET", "/changelog/{changelog}", changelog=changelog),
            params=params,
        )

    ############################## Chat

    def create_new_pm(
        self, user_id: ObjectID, msg: str, is_action: bool = True
    ) -> Response[channel.NewChannel]:
        d_json = {"target_id": user_id, "message": msg, "is_action": is_action}
        return self.request(Route("POST", "/chat/new"), json=d_json)

    def get_updates(
        self,
        channel_id: ObjectID = None,
        history_since: ObjectID = None,
        includes: str = None,
        limit: int = 10,
        since: int = None,
    ) -> Response[channel.ChannelUpdate]:
        params: Dict[str, Any] = {"limit": limit}

        if channel_id:
            params["channel_id"] = channel_id

        if history_since:
            params["history_since"] = history_since

        if includes:
            params["includes[]"] = includes

        if since:
            params["since"] = since

        return self.request(Route("GET", "/chat/updates"), params=params)

    def get_channel_messages(
        self,
        channel_id: ObjectID,
        limit: int = 10,
        since: ObjectID = None,
        until: ObjectID = None,
    ) -> Response[List[message.ChatMessage]]:
        r = Route(
            "GET", "/chat/channels/{channel}/messages", channel=channel_id
        )
        params: Dict[str, Any] = {"limit": limit}

        if since:
            params["since"] = since

        if until:
            params["until"] = until

        return self.request(r, params=params)

    def send_message_to_channel(
        self, channel_id: ObjectID, message: str, is_action: bool = True
    ) -> Response[message.ChatMessage]:
        r = Route(
            "POST", "/chat/channels/{channel}/messages", channel=channel_id
        )
        d_json = {"message": message, "is_action": is_action}

        return self.request(r, json=d_json)

    def join_channel(
        self, channel: str, user: str
    ) -> Response[channel.ChatChannel]:
        return self.request(
            Route(
                "PUT",
                "/chat/channels/{channel}/users/{user}",
                channel=channel,
                user=user,
            )
        )

    def leave_channel(self, channel: str, user: str) -> None:
        return self.request(
            Route(
                "DELETE",
                "/chat/channels/{channel}/users/{user}",
                channel=channel,
                user=user,
            )
        )

    def mark_channel_as_read(
        self,
        channel: str,
        message: str,
        channel_id: ObjectID = None,
        message_id: ObjectID = None,
    ) -> None:
        r = Route(
            "PUT",
            "/chat/channels/{channel}/mark-as-read/{message}",
            channel=channel,
            message=message,
        )
        params: Dict[str, Any] = (
            {"channel_id": channel_id, "message_id": message_id}
            if channel_id or message_id
            else None
        )

        return self.request(r, params=params)

    def get_channel_list(self) -> Response[List[channel.ChatChannel]]:
        return self.request(Route("GET", "/chat/channels"))

    def create_channel(
        self, type: str = "PM", target_id: ObjectID = None
    ) -> Response[channel.ChatChannel]:
        d_json = {"type": type}

        if target_id:
            d_json["target_id"] = target_id

        return self.request(Route("POST", "/chat/channels"), json=d_json)

    def get_channel(self, channel: str) -> Response[channel.DetailedChannel]:
        return self.request(
            Route("GET", "/chat/channels/{channel}", channel=channel)
        )

    def get_channel_presence(self) -> Response[List[channel.NewChannel]]:
        return self.request(Route("GET", "/chat/presence"))

    ############################## Comments

    def get_comments(
        self,
        commentable_type: str = None,
        commentable_id: ObjectID = None,
        cursor: str = None,
        parent_id: ObjectID = 0,
        sort: str = "new",
    ) -> Response[comment.CommentBundle]:
        params: Dict[str, Any] = {
            "parent_id": parent_id,
            "sort": sort,
        }

        if commentable_type:
            params["commentable_type"] = commentable_type

        if commentable_id:
            params["commentable_id"] = commentable_id

        if cursor:
            params["cursor"] = cursor

        return self.request(Route("GET", "/comments"), params=params)

    def post_new_comment(
        self,
        commentable_id: ObjectID = None,
        commentable_type: str = None,
        message: str = None,
        parent_id: ObjectID = None,
    ) -> Response[comment.CommentBundle]:
        params: Dict[str, Any] = {
            "comment.commentable_id": commentable_id,
            "comment.commentable_type": commentable_type,
            "comment.message": message,
            "comment.parent_id": parent_id,
        }

        return self.request(Route("POST", "/comments"), params=params)

    def get_comment(self, comment: str) -> Response[comment.CommentBundle]:
        return self.request(
            Route("GET", "/comments/{comment}", comment=comment)
        )

    def edit_comment(
        self, comment: str, comment_message: str = None
    ) -> Response[comment.CommentBundle]:
        params: Dict[str, Any] = (
            {"comment.message": comment_message} if comment_message else None
        )

        return self.request(
            Route("PUT", "/comments/{comment}", comment=comment), params=params
        )

    def delete_comment(self, comment: str) -> Response[comment.CommentBundle]:
        return self.request(
            Route("DELETE", "/comments/{comment}", comment=comment)
        )

    def add_comment_vote(
        self, comment: str
    ) -> Response[comment.CommentBundle]:
        return self.request(
            Route("POST", "/comments/{comment}/vote", comment=comment)
        )

    def remove_comment_vote(
        self, comment: str
    ) -> Response[comment.CommentBundle]:
        return self.request(
            Route("DELETE", "/comments/{comment}/vote", comment=comment)
        )

    ############################## Forum

    def reply_topic(
        self, topic_id: ObjectID, body: str
    ) -> Response[forum.ForumPost]:
        r = Route("POST", "/forums/topics/{topic}/reply", topic=topic_id)
        d_json = {"body": body}

        return self.request(r, json=d_json)

    def create_topic(
        self,
        body: str,
        forum_id: ObjectID,
        title: str,
        with_poll: bool = False,
        p_hide_results: bool = False,
        p_length_days: int = 0,
        p_max_options: int = 1,
        p_options: str = None,
        p_title: str = None,
        p_vote_change: bool = False,
    ) -> Response[forum.NewForumTopic]:
        d_json = {
            "body": body,
            "forum_id": forum_id,
            "title": title,
            "with_poll": with_poll,
        }

        if with_poll:
            d_json["forum_topic_poll[hide_results]"] = p_hide_results
            d_json["forum_topic_poll[length_days]"] = p_length_days
            d_json["forum_topic_poll[max_options]"] = p_max_options
            d_json["forum_topic_poll[options]"] = p_options
            d_json["forum_topic_poll[title]"] = p_title
            d_json["forum_topic_poll[vote_change]"] = p_vote_change

        return self.request(Route("POST", "/forums/topics"), json=d_json)

    def get_topic_with_posts(
        self,
        topic_id: ObjectID,
        cursor: str = None,
        sort: str = "id_desc",
        limit: int = 10,
        start: str = None,
        end: str = None,
    ) -> Response[forum.ForumNavigation]:
        params: Dict[str, Any] = {
            "sort": sort,
            "limit": limit,
        }

        if cursor:
            params["cursor_string"] = cursor

        if start:
            params["start"] = start

        if end:
            params["end"] = end

        return self.request(
            Route("GET", "/forums/topics/{topic}", topic=topic_id),
            params=params,
        )

    def edit_topic(
        self, topic_id: ObjectID, title: str = None
    ) -> Response[forum.ForumTopic]:
        d_json = {"forum_topic[topic_title]": title} if title else None
        return self.request(
            Route("PUT", "/forums/topics/{topic}", topic=topic_id), json=d_json
        )

    def edit_post(
        self, post_id: ObjectID, body: str
    ) -> Response[forum.ForumPost]:
        d_json = {"body": body}
        return self.request(
            Route("PUT", "/forums/posts/{post}", post=post_id), json=d_json
        )

    ############################## Home

    def search(
        self, mode: str = "all", page: int = 1, query: str = None
    ) -> Union[Response[wiki.WikiPage], Response[user.User]]:
        params: Dict[str, Any] = {"mode": mode, "page": page}

        if query:
            params["query"] = query

        return self.request(Route("GET", "/search"), params=params)

    ############################## Multiplayer

    def get_user_highscore(
        self, room_id: ObjectID, playlist_id: ObjectID, user_id: ObjectID
    ) -> Response[multiplayer.MultiplayerScore]:
        r = Route(
            "GET",
            "/rooms/{room}/playlist/{playlist}/scores/users/{user}",
            room=room_id,
            playlist=playlist_id,
            user=user_id,
        )

        return self.request(r)

    def get_scores(
        self,
        room_id: ObjectID,
        playlist_id: ObjectID,
        limit: int = 10,
        sort: str = None,
        cursor: str = None,
    ) -> Response[multiplayer.MultiplayerScoreList]:
        params: Dict[str, Any] = {"limit": limit}

        if sort:
            params["sort"] = sort

        if cursor:
            params["cursor"] = cursor

        return self.request(
            Route(
                "GET",
                "/rooms/{room}/playlist/{playlist}/scores",
                room=room_id,
                playlist=playlist_id,
            ),
            params=params,
        )

    def get_specific_score(
        self, room_id: ObjectID, playlist_id: ObjectID, score_id: ObjectID
    ) -> Response[multiplayer.MultiplayerScore]:
        r = Route(
            "GET",
            "/rooms/{room}/playlist/{playlist}/scores/{score}",
            room=room_id,
            playlist=playlist_id,
            score=score_id,
        )

        return self.request(r)

    ############################## News

    def get_news_listing(
        self, limit: int = 12, year: int = None, cursor: str = None
    ) -> Response[news.NewsPostList]:
        params: Dict[str, Any] = {"limit": limit}

        if year:
            params["year"] = year

        if cursor:
            params["cursor"] = cursor

        return self.request(Route("GET", "/news"), params=params)

    def get_news_post(
        self, news: str, key: str = None
    ) -> Response[news.NewsPost]:
        params: Dict[str, Any] = {"key": key} if key else {}
        return self.request(
            Route("GET", "/news/{news}", news=news), params=params
        )

    ############################## Notifications

    def get_notifications(
        self, max_id: str = "sint"
    ) -> Response[notifications.NotificationList]:
        params: Dict[str, str] = {"max_id": max_id}

        return self.request(Route("GET", "/notifications"), params=params)

    def read_notifications(self, notification_ids: List[ObjectID]):
        d_json = {"ids": notification_ids}
        return self.request(
            Route("POST", "/notifications/mark-read"), json=d_json
        )

    ############################## OAuth

    def delete_current_token(self) -> None:
        return self.request(Route("DELETE", "/oauth/tokens/current"))

    ############################# Ranking

    def get_rankings(
        self,
        mode: str = "osu",
        type: str = "score",
        country: bool = False,
        cursor: str = None,
        filter: str = "all",
        spotlight: str = None,
        variant: str = None,
    ) -> Response[rankings.Rankings]:
        params: Dict[str, Any] = {"mode": mode, "type": type}

        if type == "performance":
            params["country"] = country
            params["variant"] = variant

        if type == "charts":
            params["spotlight"] = spotlight

        if cursor:
            params["cursor"] = cursor

        if filter:
            params["filter"] = filter

        return self.request(
            Route("GET", "/rankings/{mode}/{type}", mode=mode, type=type),
            params=params,
        )

    def get_spotlights(self) -> Response[List[rankings.Spotlight]]:
        return self.request(Route("GET", "/spotlights"))

    ########################### User

    def get_own_user(self, mode: Optional[str] = None) -> Response[user.User]:
        if mode:
            r = Route("GET", "/me/{mode}", mode=mode)
        else:
            r = Route("GET", "/me")

        return self.request(r)

    def get_user_kudosu(
        self,
        user_id: ObjectID,
        limit: int = 10,
        offset: int = 0,
    ) -> Response[List[kudosu.KudosuHistory]]:
        params: Dict[str, Any] = {"limit": limit, "offset": offset}

        return self.request(
            Route("GET", "/users/{user}/kudosu", user=user_id), params=params
        )

    def get_user_scores(
        self,
        user_id: ObjectID,
        type: str,
        include_fails: bool = False,
        mode: str = "osu",
        limit: int = 10,
        offset: int = 0,
    ) -> Response[List[score.Score]]:
        params: Dict[str, Any] = {
            "include_fails": 1 if include_fails else 0,
            "mode": mode,
            "limit": limit,
            "offset": offset,
        }

        r = Route(
            "GET", "/users/{user}/scores/{type}", user=user_id, type=type
        )

        return self.request(r, params=params)

    def get_user_beatmaps(
        self, user_id: ObjectID, type: str, limit: int = 10, offset: int = 0
    ) -> Response[List[beatmap.Beatmapset]]:
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        r = Route(
            "GET", "/users/{user}/beatmapsets/{type}", user=user_id, type=type
        )
        return self.request(r, params=params)

    def get_user_recent_activity(
        self, user_id: ObjectID, limit: int = 10, offset: int = 0
    ) -> Response[List[event.Event]]:
        params: Dict[str, Any] = {"limit": limit, "offset": offset}

        r = Route("GET", "/users/{user}/recent_activity", user=user_id)
        return self.request(r, params=params)

    def get_user(
        self,
        user_id: ObjectID,
        mode: Optional[str] = None,
        key: Optional[str] = "id",
    ) -> Response[user.User]:
        params: Dict[str, Any] = {"key": key}

        if mode:
            r = Route("GET", "/users/{user}/{mode}", user=user_id, mode=mode)
        else:
            r = Route("GET", "/users/{user}", user=user_id)

        return self.request(r, params=params)

    def get_users(self, users: List[ObjectID]) -> Response[List[user.User]]:
        params = "&".join([f"ids[]={str(x)}" for x in users])
        path = f"/users?{params}"

        return self.request(Route("GET", path))

    ################################### Wiki

    def get_wiki_page(
        self, locale: str = "en", path: str = "Welcome"
    ) -> Response[wiki.WikiPage]:
        return self.request(
            Route("GET", "/wiki/{locale}/{path}", locale=locale, path=path)
        )
