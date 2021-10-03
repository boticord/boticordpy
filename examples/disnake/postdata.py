from discord.ext import commands

from boticordpy import BoticordClient

bot = commands.Bot(command_prefix="!")
boticord = BoticordClient(bot, "your-boticord-token", lib="disnake")


@bot.event
async def on_ready():
    await boticord.Bots.post_stats()


bot.run("your-bot-token")
