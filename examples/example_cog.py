from discord.ext import commands

from boticordpy import BoticordClient


class BoticordCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.boticord = BoticordClient(self.bot, "your-boticord-token")
        self.boticord.start_loop()

    @commands.command(name="boticord-update")
    @commands.is_owner()
    async def boticord_update(self, ctx):
        """
            This commands can be used by owner to post stats to boticord
        """
        stats = {"servers": len(self.bot.guilds), "shards": 0, "users": len(self.bot.users)}
        await self.boticord.Bots.post_stats(stats)


def setup(bot):
    bot.add_cog(BoticordCog(bot))
