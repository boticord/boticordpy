<p align="center">
<img width="560" src="https://github.com/boticord/boticordpy/assets/61203964/87393a07-2afa-4568-a324-500d1940b4fc" alt="">
</p>

<p align="center">
  <b>
    The easiest way to use BotiCord API in Python.
    <span> · </span>
    <a href="https://py.boticord.top/">Docs</a>
  </b>
</p>

<p align="center">
<a href="https://pypi.org/project/boticordpy/"><img src="https://img.shields.io/pypi/dm/boticordpy?style=flat-square" alt=""></a>
<a href="https://pypi.org/project/boticordpy/"><img src="https://img.shields.io/pypi/v/boticordpy?style=flat-square" alt=""></a>
<a href="https://py.boticord.top/"><img src="https://img.shields.io/readthedocs/boticordpy?style=flat-square" alt=""></a>
</p>


<h2>Features</h2>

* Object-oriented
* Full BotiCord API Coverage
* Modern Pythonic API using `async`/`await` syntax
* BotiCord Websocket
* It is not necessary to use any particular library used to interact with the Discord API.

<h2>Installation</h2>

<b>Python 3.8 or newer is required.</b>

Enter one of these commands to install the library:

```
pip install boticordpy
```

```
python3 -m pip install boticordpy
```

Or just clone the repo: https://github.com/boticord/boticordpy

<h2>Examples</h2>

You can find other examples in an examples folder. 

**Discord.py Autopost example**

```py
from discord.ext import commands
from boticordpy import BoticordClient

bot = commands.Bot(command_prefix="!")


# Function that will return the current bot's stats.
async def get_stats():
    return {"servers": len(bot.guilds), "shards": None, "members": len(bot.users)}


# Function that will be called if stats are posted successfully.
async def on_success_posting():
    print("wow stats posting works")


boticord_client = BoticordClient(
    "your_boticord_api_token", version=3
)  # <--- BotiCord API token
autopost = (
    boticord_client.autopost()
    .init_stats(get_stats)
    .on_success(on_success_posting)
    .start("id_of_your_bot")  # <--- ID of your bot
)

bot.run("bot token")  # <--- Discord bot's token

```

<h2>Links</h2>

* [PyPi](https://pypi.org/project/boticordpy)
* [Documentation](https://py.boticord.top)
* [Github](https://github.com/boticord/boticordpy)
* [BotiCord](https://boticord.top/)
* [Support](https://boticord.top/discord)

<h2>Help</h2>

If You need any help we recommend you to check the documentation. You can find us [here](https://bcord.cc/support). Main developer is **[Marakarka](https://boticord.top/profile/585766846268047370)**
