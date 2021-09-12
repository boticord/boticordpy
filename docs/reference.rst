.. currentmodule:: boticordpy

.. reference:

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

.. function:: new_bot_bump

    Called when the user bumps the bot.

    Return Example: ``{'type': 'new_bot_bump', 'data': {'user': '809377165534822410', 'at': 1631436624444}}``

.. function:: new_bot_comment

    Called when the user creates new comment.

    Return Example: ``{'type': 'new_bot_comment', 'data': {'user': '704373738086465607', 'comment': {'old': None, 'new': 'boticord po jizni top'}, 'at': 1631439995678}}
``


.. function:: edit_bot_comment

    Called when the user edits his comment.

    Return Example: ``{'type': 'edit_bot_comment', 'data': {'user': '585766846268047370', 'comment': {'old': 'Boticord eto horosho', 'new': 'Boticord horoshiy monitoring'}, 'at': 1631438224813}}``

.. function:: delete_bot_comment

    Called when the user deletes his comment.

    Return Example:
        {'type': 'delete_bot_comment', 'data': {'user': '704373738086465607', 'comment': 'допустим что я картофель', 'vote': 1, 'reason': 'self', 'at': 1631439759384}}
