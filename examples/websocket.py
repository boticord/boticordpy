# You can use any library to interact with the Discord API.
# This example uses discord.py.
# You can install it with `pip install discord.py`.

from discord.ext import commands
from boticordpy import BotiCordWebsocket

bot = commands.Bot(command_prefix="!")

websocket = BotiCordWebsocket("your_boticord_api_token")  # <--- BotiCord API token


@websocket.listener()
async def comment_removed(data):
    print(data["payload"])


@bot.event
async def on_ready():
    await websocket.connect()


bot.run("bot token")  # <--- Discord bot's token
