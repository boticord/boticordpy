import melisa
from boticordpy import BoticordClient

bot = melisa.Bot("your_discord_bot_token")

boticord = BoticordClient("your_boticord_api_token")


@bot.listen
async def on_message_create(message):
    if message.content.startswith("!guilds"):
        data = await boticord.get_bot_info(bot.user.id)
        await bot.rest.create_message(message.channel.id, data.guilds)


bot.run_autosharded()
