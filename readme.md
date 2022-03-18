python-osu - Unofficial Library
========
An easy to use, asynchronous API wrapper for osu!api v2

Features
--------
- Asynchronous calls to osu!api v2 endpoints.
- Access to lazer routes and all scopes.
- Uses public client credentials.

Note
----
Currently this library is under development and many functions still need to be handled and packed properly into objects with their methods. Although, all documented api calls can be called directly through `pyosu.HttpClient` object inside `pyosu.Client`.

```python
...
await client.http.get_user()
await client.http.create_channel()
await client.http.get_user_beatmap_score()
...
```

To-do list
----------
- <s>Cache for PM Channels and other objects such as Scores</s>
- <s>Client access to changelog calls</s>
- <s>Add mark_as_read() to ChatChannel</s>
- Client access to comments calls
- <s>Client access to forum calls</s>
- <s>Client access to search wiki calls</s>
- Client access to news calls
- Client access to users, wiki and ranking calls

Installing
----------
**Python 3.9 or higher is required for this library.**

Check requeriments.txt


Run the following command for installation:

```sh
git clone https://github.com/grapphy/python-osu
cd python-osu
pip install .
```

Authentication
--------------
To use this api you need to authenticate yourself to get a token. There are 3 ways to achieve this:

- Using the official osu public client credentials
    ```python
    await client.public_login() # No input of your own required
    ```
- Using your personal client credentials
    ```python
    await client.oauth_login("CLIENT_ID", "CLIENT_SECRET")
    ```
- Using your username and password
    ```python
    await client.login("username", "password")
    ```

Note that if you choose to use any client credentials you might not be able to access all calls from this library, since some of them are only for osu!lazer scope (which only works with username and password authentication)

Quick Example
-------------
```python
import asyncio
from pyosu import Client

# Osu Client
client = Client()

async def example_client():
    # Login client
    await client.login("username", "password")
    print(f"Connected as: {client.user.username}")

    # Getting a beatmapset by ID
    beatmapset = await client.fetch_beatmapset(1551253)
    # |beatmapset.id
    # |beatmapset.creator
    # |beatmapset.title
    # |beatmapset.beatmaps[0].id
    # |beatmapset.beatmaps[0].mode
    # |beatmapset.beatmaps[0].status

    # Getting a beatmap by ID
    beatmap = await client.fetch_beatmap(139919)
    # |beatmap.id
    # |beatmap.mode
    # |beatmap.status
    # |beatmap.version

    # Getting scores from a beatmap object
    scores = await beatmap.fetch_scores()
    # |scores[0].id
    # |scores[0].accuracy
    # |scores[0].rank
    # |scores[0].score

    user = await client.fetch_user(146121)
    # |user.id
    # |user.username
    # |user.country_code
    # |user.is_active

    # Sending PMs
    msg = await user.send("hello")
    # |msg.id
    # |msg.sender_id
    # |msg.timestamp
    # |msg.content

    # Reading PM messages
    async for message in user.pm_channel.history(limit=None):
        print(f"{message.sender.username}: {message.content}")

    # Closing the connection
    await client.logout()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(example_client())
```

Fetching changelogs
-------------
```python
import asyncio
import pyosu

# Osu Client
client = pyosu.Client()

async def example_build_fetch():
    # Login with public credentials
    await client.public_login()

    # Fetching changelog from a build
    build = await client.fetch_build_changelog(
        pyosu.ChangelogStream.Stable, "20160403.5"
    )

    print("Build id:", build.id)
    print("Stream name:", build.update_stream.name)
    print("Stream id:", build.update_stream.id)

    # Fetching changelog from a stream
    changelog = await client.fetch_changelog(pyosu.ChangelogStream.Stable)
    print(changelog)

    # Closing the connection
    await client.logout()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(example_build_fetch())
```

Interacting with forums
-----------------------
```python
import asyncio
import pyosu

# Osu Client
client = pyosu.Client()

async def example_forums():
    # Login client
    await client.login("username", "password")
    print(f"Connected as: {client.user.username}")

    # Fetching a forum thread
    topic = await client.fetch_topic(1535730)

    # Fetching replies from a thread
    async for post in topic.fetch_posts(limit=5):
        parsed_msg = post.raw.split("]")[-1] # Removing BBCode
        print(f"{parsed_msg!r}")

    # Replying to a thread
    reply = await topic.reply("This is a reply to a thread")

    # Creating a poll object
    poll_options = [
        pyosu.ForumOption.create("Option one"),
        pyosu.ForumOption.create("Option two"),
        pyosu.ForumOption.create("Option three"),
        pyosu.ForumOption.create("Option four"),
    ]

    mypoll = pyosu.ForumPoll.create("This a test poll", poll_options)

    # Creating a topic with poll
    mytopic = await client.create_topic(
        52,
        "This a test thread",
        "This is the body of a test thread",
        poll=mypoll,
    )

    # Closing the connection
    await client.logout()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(example_forums())
```

License
-------
This project is under the [MIT License](https://mit-license.org/).

Credits
-------
For educational and informational purposes.

Feel free to contribute/distribute/etc any piece of code from this repository.