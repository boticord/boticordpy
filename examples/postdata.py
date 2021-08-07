from discord.ext import commands

from boticordpy import BoticordClient

bot = commands.Bot(command_prefix="!")
boticord = BoticordClient(bot, token="your-boticord-token")


@bot.event
async def on_connect():
    stats = {"servers": len(bot.guilds), "shards": bot.shard_count, "users": len(bot.users)}
    await boticord.Bots.postStats(stats)


bot.run("your-bot-token")