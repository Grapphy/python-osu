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

# Python standard libraries
import json
import aiohttp
from collections import OrderedDict

# Global variables
osu = "https://osu.ppy.sh"


async def create_osu_account(
    username: str, password: str, email: str = None
) -> dict:
    headers = OrderedDict(
        (
            ("User-Agent", "osu!"),
            (
                "Accept",
                "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            ),
            ("Accept-Language", "en-US;q=0.5,en;q=0.3"),
            ("Accept-Encoding", "gzip, deflate"),
            ("Content-Type", "application/json"),
        )
    )

    async with aiohttp.ClientSession(headers=headers) as session:
        uri = f"{osu}/users"
        payload = {
            "user": {
                "username": username,
                "user_email": email,
                "password": password,
            }
        }

        async with session.post(uri, data=json.dumps(payload)) as res:
            r_json = await res.json()

            if "form_error" in r_json:
                raise Exception(r_json.get("form_error"))

            return r_json
