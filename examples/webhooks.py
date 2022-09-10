# You can use any library to interact with the Discord API.
# This example uses discord.py.
# You can install it with `pip install discord.py`.

from discord.ext import commands
from boticordpy import webhook

bot = commands.Bot(command_prefix="!")


async def edit_bot_comment(data):
    print(data.comment.new)


boticord_webhook = webhook.Webhook("x-hook-key", "bot").register_listener(
    "edit_bot_comment", edit_bot_comment
)
boticord_webhook.start(5000)

bot.run("bot_token")
