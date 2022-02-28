import asyncio
import unittest
import dotenv
import os

import random
import json

from osu.http import HTTPClient

# Load enviroment variables
dotenv.load_dotenv()


class TestUserCall(unittest.TestCase):
    """For testing all queries related to osu! users."""

    @classmethod
    def setUpClass(cls):
        cls.client_username = os.getenv("TEST_CLIENT_USER")
        cls.client_password = os.getenv("TEST_CLIENT_PASS")
        cls.test_users = json.loads(os.getenv("TEST_USERS"))

        cls.http = HTTPClient()
        cls.loop = asyncio.new_event_loop()

        cls.loop.run_until_complete(
            cls.http.oauth_login(
                grant_type="password",
                scope="*",
                username=cls.client_username,
                password=cls.client_password,
            )
        )

    def test_get_own_user(self):
        response = self.loop.run_until_complete(self.http.get_own_user())
        self.assertIn("username", response)
        self.assertEqual(self.client_username, response.get("username"))

    def test_get_user_kudosu(self):
        test_user = random.choice(self.test_users["kudosu"])
        response = self.loop.run_until_complete(
            self.http.get_user_kudosu(test_user)
        )

        self.assertIsInstance(response, list)

    def test_get_user_scores(self):
        test_user = random.choice(self.test_users["general"])
        test_type = random.choice(self.test_users["play_types"])
        response = self.loop.run_until_complete(
            self.http.get_user_scores(test_user, type=test_type)
        )

        self.assertIsInstance(response, list)

    def test_get_user_beatmaps(self):
        test_user = random.choice(self.test_users["general"])
        test_type = random.choice(self.test_users["beatmap_types"])
        response = self.loop.run_until_complete(
            self.http.get_user_beatmaps(test_user, type=test_type)
        )

        self.assertIsInstance(response, list)

    def test_get_user_recent_activity(self):
        test_user = random.choice(self.test_users["general"])
        response = self.loop.run_until_complete(
            self.http.get_user_recent_activity(test_user)
        )

        self.assertIsInstance(response, list)

    def test_get_user(self):
        test_user = random.choice(self.test_users["general"])
        response = self.loop.run_until_complete(self.http.get_user(test_user))

        self.assertIn("id", response)
        self.assertEqual(test_user, response.get("id"))

    def test_get_users(self):
        test_users = self.test_users["general"]
        response = self.loop.run_until_complete(
            self.http.get_users(test_users)
        )

        self.assertIn("users", response)
        self.assertEqual(len(response.get("users")), len(test_users))

    @classmethod
    def tearDownClass(cls):
        cls.loop.run_until_complete(cls.http.close_session())


if __name__ == "__main__":
    unittest.main()
