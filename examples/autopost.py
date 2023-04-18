# You can use any library to interact with the Discord API.
# This example uses discord.py.
# You can install it with `pip install discord.py`.

from discord.ext import commands
from boticordpy import BoticordClient

bot = commands.Bot(command_prefix="!")


# Function that will return the current bot's stats.
async def get_stats():
    return {"servers": len(bot.guilds), "shards": 0, "users": len(bot.users)}


# Function that will be called if stats are posted successfully.
async def on_success_posting():
    print("stats posting successfully")


boticord_client = BoticordClient("Bot your_api_token", version=2)
autopost = (
    boticord_client.autopost()
    .init_stats(get_stats)
    .on_success(on_success_posting)
    .start()
)

bot.run("bot token")
