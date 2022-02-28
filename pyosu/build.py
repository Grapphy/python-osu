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
