# You can use any library to interact with the Discord API.
# This example uses discord.py.
# You can install it with `pip install discord.py`.

from discord.ext import commands
from boticordpy import BoticordClient

bot = commands.Bot(command_prefix="!")


# Function that will return the current bot's stats.
async def get_stats():
    return {"guilds": len(bot.guilds), "shards": 0, "members": len(bot.users)}


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
