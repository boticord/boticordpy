from discord.ext import commands

from boticordpy import BoticordWebhook, BoticordClient

bot = commands.Bot(command_prefix="!")
boticord = BoticordClient(bot, "boticord-api-token")

boticord_webhook = BoticordWebhook(bot, boticord).bot_webhook("/bot", "X-Hook-Key")
boticord_webhook.run(5000)


@boticord.event("edit_bot_comment")
async def on_boticord_comment_edit(data):
    print(data)

bot.run("bot-token")