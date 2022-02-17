<p align="center">
<img width="520" src="https://media.discordapp.net/attachments/825242846616354821/939773822582808606/boticordrs_banner.png" alt="">
</p>

<p align="center">
  <b>
    The easiest way to use Boticord API in Python.
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
* Full Boticord API Coverage
* Modern Pythonic API using `async`/`await` syntax
* Boticord Webhooks
* It is not necessary to use any particular library to interact with the Discord API.

<h2>Installation</h2>

<b>Python 3.6 or newer is required.</b>

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


    async def get_stats():
        return {"servers": len(bot.guilds), "shards": 0, "users": len(bot.users)}


    async def on_success_posting():
        print("stats posting successfully")

    boticord_client = BoticordClient("your_api_token")
    autopost = (
        boticord_client.autopost()
        .init_stats(get_stats)
        .on_success(on_success_posting)
    )

    bot.run("bot token")
```

<h2>Links</h2>

* [PyPi](https://pypi.org/project/boticordpy)
* [Documentation](https://py.boticord.top)
* [Github](https://github.com/boticord/boticordpy)
* [Boticord](https://boticord.top/)
* [Support](https://boticord.top/boticord)

<h2>Help</h2>

If You need any help we recommend you to check the documentation. You can find us [here](https://boticord.top/boticord). Main developer `Marakarka#0575`
