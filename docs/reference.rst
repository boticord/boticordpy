.. currentmodule:: boticordpy

.. reference:

Reference
==============

Event Reference
---------------
Example of event creation:

::

    from discord.ext import commands

    from boticordpy import BoticordWebhook, BoticordClient

    bot = commands.Bot(command_prefix="!")
    boticord = BoticordClient(bot, "boticord-api-token")

    boticord_webhook = BoticordWebhook(bot, boticord).bot_webhook("/bot", "X-Hook-Key")
    boticord_webhook.run(5000)


    @boticord.event("edit_bot_comment")
    async def on_boticord_comment_edit(data):
        print(data)


You can name the function whatever you want, but the decorator must always specify an existing event as an argument.

.. warning::

    All the events must be a **coroutine**. If they aren't, then you might get unexpected
    errors. In order to turn a function into a coroutine they must be ``async def``
    functions.

Here you can find some information about events:

+------------------------+----------------------------------+
|    Boticord Events     |            Returns Type          |
+========================+==================================+
|    new_bot_comment     |           types.Comment          |
+------------------------+----------------------------------+
|    edit_bot_comment    |        types.EditedComment       |
+------------------------+----------------------------------+
|   delete_bot_comment   |           types.Comment          |
+------------------------+----------------------------------+
|      new_bot_bump      |           types.BotVote          |
+------------------------+----------------------------------+
|   new_server_comment   |             Raw Data             |
+------------------------+----------------------------------+
|   edit_server_comment  |             Raw Data             |
+------------------------+----------------------------------+
|  delete_server_comment |             Raw Data             |
+------------------------+----------------------------------+

You can find more events in Boticord Documentation.


Types
------------
.. automodule:: boticordpy.types
   :members:
