# You can use disnake or nextcord or something like this.
# (THIS EXAMPLE IS NOT TESTED. IF YOU HAVE ANY PROBLEMS - ASK DEVELOPER PLEASE)

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
