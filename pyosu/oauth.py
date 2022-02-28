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
from typing import Any, ClassVar, Optional

import json
import aiohttp


class OAuth:
    CLIENT_ID: ClassVar[int] = 5
    BASE: ClassVar[str] = "https://osu.ppy.sh/oauth/token"
    # Public credentials for osu!lazer
    CLIENT_SECRET: ClassVar[str] = "FGc9GAtyHzeQDshWP5Ah7dega8hJACAJpQtw6OXk"

    def __init__(
        self,
        grant_type: Optional[str] = None,
        scope: Optional[str] = None,
        **parameters: Any
    ) -> None:
        self.grant_type = grant_type or "client_credentials"
        self.scope = scope or "public"
        self.data = {
            **{
                "client_id": parameters.get("client_id", self.CLIENT_ID),
                "client_secret": parameters.get(
                    "client_secret", self.CLIENT_SECRET
                ),
                "grant_type": self.grant_type,
                "scope": self.scope,
            },
            **parameters,
        }

    @property
    def payload(self) -> str:
        return json.dumps(self.data)

    async def authenticate(
        self, session: aiohttp.ClientSession, **kwargs
    ) -> str:
        kwargs["headers"] = {
            "User-Agent": kwargs.pop("user_agent", "osu!"),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        kwargs["data"] = self.payload

        async with session.post(self.BASE, **kwargs) as res:
            return await res.json()
