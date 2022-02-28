import asyncio
import unittest
import dotenv
import os

import random
import json

from osu.http import HTTPClient

# Load enviroment variables
dotenv.load_dotenv()


class TestBeatmapCall(unittest.TestCase):
    """For testing all queries related to /beatmaps route."""

    @classmethod
    def setUpClass(cls):
        cls.client_username = os.getenv("TEST_CLIENT_USER")
        cls.client_password = os.getenv("TEST_CLIENT_PASS")
        cls.test_users = json.loads(os.getenv("TEST_USERS"))

        cls.http = HTTPClient(
            proxy="http://127.0.0.1:8080",
            ssl=False,
        )
        cls.loop = asyncio.new_event_loop()

        cls.loop.run_until_complete(
            cls.http.oauth_login(
                grant_type="password",
                scope="*",
                username=cls.client_username,
                password=cls.client_password,
            )
        )

    def test_lookup_beatmap(self):
        map_id = 139919
        response = self.loop.run_until_complete(
            self.http.lookup_beatmap(map_id=map_id)
        )

        self.assertIn("id", response)
        self.assertEqual(map_id, response.get("id"))

    def test_get_user_beatmap_score(self):
        map_id = 139919
        user_id = 329839
        response = self.loop.run_until_complete(
            self.http.get_user_beatmap_score(map_id, user_id)
        )

        self.assertIn("score", response)
        self.assertIn("beatmap", response["score"])
        self.assertEqual(map_id, response["score"]["beatmap"]["id"])
        self.assertEqual(user_id, response["score"]["user_id"])

    def test_get_beatmap_score(self):
        map_id = 139919
        response = self.loop.run_until_complete(
            self.http.get_beatmap_scores(map_id)
        )

        self.assertIn("scores", response)
        self.assertIsInstance(response["scores"], list)

    def test_get_beatmaps(self):
        maps = [142590, 220792]
        response = self.loop.run_until_complete(self.http.get_beatmaps(maps))

        self.assertIn("beatmaps", response)
        self.assertIsInstance(response["beatmaps"], list)
        self.assertEqual(len(response["beatmaps"]), 2)

    def test_get_beatmap(self):
        map_id = 139919
        response = self.loop.run_until_complete(self.http.get_beatmap(map_id))

        self.assertIn("id", response)
        self.assertEqual(response["id"], map_id)

    @classmethod
    def tearDownClass(cls):
        cls.loop.run_until_complete(cls.http.close_session())


if __name__ == "__main__":
    unittest.main()
