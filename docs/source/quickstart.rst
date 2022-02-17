.. currentmodule:: boticordpy

.. quickstart:

Quickstart
==========

**For more examples or information about other features check Github-Repo.**

Installation
------------

Enter one of these commands to install the library:

::

    pip install boticordpy


::

    python3 -m pip install boticordpy


Or just clone the repo: https://github.com/boticord/boticordpy



Examples
-------------------------

**Discord.py Autopost example**

::

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
        .start()
    )

    bot.run("bot token")


..


**Discord.py Webhooks example**

::

    from discord.ext import commands

    from boticordpy import webhook

    bot = commands.Bot(command_prefix="!")


    async def edit_bot_comment(data):
        print(data.comment.new)

    boticord_webhook = webhook.Webhook("x-hook-key", "bot").register_listener("edit_bot_comment", edit_bot_comment)
    boticord_webhook.start(5000)

    bot.run("bot token")


..


