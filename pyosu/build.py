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

from .types.build import Build as BuildPayload
from .types.build import Versions as VersionsPayload
from .types.build import UpdateStream as UpdateStreamPayload


class UpdateStream:
    def __init__(self, *, data: UpdateStreamPayload) -> None:
        self._update_data(data)

    def _update_data(self, data: UpdateStreamPayload) -> None:
        self.id = data["id"]
        self.name = data["name"]
        self.display_name = data["display_name"]
        self.is_featured = data["is_featured"]
        self.latest_build = data.get("latest_build")
        self.user_count = data.get("user_count")


class Versions:
    def __init__(self, *, data: VersionsPayload) -> None:
        self._update_data(data)

    def _update_data(self, data: VersionsPayload) -> None:
        if "previous" in data:
            self.previous = BuildChangelog(data=data["previous"])

        if "next" in data:
            self.next = BuildChangelog(data=data["next"])


class BuildChangelog:
    def __init__(self, *, data: BuildPayload) -> None:
        self._update_data(data)

    def _update_data(self, data: BuildPayload) -> None:
        self.id = data["id"]
        self.version = data["version"]
        self.display_version = data["display_version"]
        self.users = data["users"]
        self.created_at = data["created_at"]
        self.update_stream = self._handle_update_stream(data["update_stream"])

        self.changelog_entries = data.get("changelog_entries")
        self.versions = self._handle_versions(data.get("versions"))

    def _handle_update_stream(self, data: UpdateStreamPayload) -> UpdateStream:
        return UpdateStream(data=data)

    def _handle_versions(self, data: VersionsPayload) -> Versions:
        return Versions(data=data) if data else None
