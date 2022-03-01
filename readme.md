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
- Client access to forum calls
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
    channel = await user.create_pm("hello")
    # |channel.id
    # |channel.name
    # |channel.last_read_id

    msg = await channel.send("how are you")
    # |msg.id
    # |msg.sender_id
    # |msg.timestamp
    # |msg.content

    print(f"Message {msg.content!r} sent to {channel.id}")

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
from pyosu import Client

# Osu Client
client = Client()

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

License
-------
This project is under the [MIT License](https://mit-license.org/).

Credits
-------
For educational and informational purposes.

Feel free to contribute/distribute/etc any piece of code from this repository.