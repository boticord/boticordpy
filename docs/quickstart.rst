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



Examples
-------------------------

**Without Using Cogs System**

Post bot stats when bot is ready.

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

**Using Cogs System**

Cog with automatically stats post (every 15 minutes) + bot's owner command that can be used to post stats.

::

    from discord.ext import commands

    from boticordpy import BoticordClient


    class BoticordCog(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
            self.boticord = BoticordClient(self.bot, "your-boticord-token")
            self.boticord.start_loop()

        @commands.command(name="boticord-update")
        @commands.is_owner()
        async def boticord_update(self, ctx):
            """
                This commands can be used by owner to post stats to boticord
            """
            stats = {"servers": len(self.bot.guilds), "shards": 0, "users": len(self.bot.users)}
            await self.boticord.Bots.postStats(stats)


    def setup(bot):
        bot.add_cog(BoticordCog(bot))

..
