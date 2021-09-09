.. currentmodule:: boticordpy

.. quickstart:

Quickstart
==========

Installation
------------

Enter one of these commands to install the library:

::

    pip install boticordpy


::

    python3 -m pip install boticordpy


Or just clone the repo: https://github.com/grey-cat-1908/boticordpy



Post Bot Stats
-------------------------

Let's post our bot's stats to Boticord.

::

    from discord.ext import commands

    from boticordpy import BoticordClient

    bot = commands.Bot(command_prefix="!")
    boticord = BoticordClient(bot, "your-boticord-token")


    @bot.event
    async def on_ready():
        stats = {"servers": len(bot.guilds), "shards": bot.shard_count, "users": len(bot.users)}
        await boticord.Bots.postStats(stats)


    bot.run("your-bot-token")

..