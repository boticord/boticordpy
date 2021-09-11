from discord.ext import commands
from typing import Union
import asyncio
import aiohttp

from .modules import Bots, Servers, Users


class BoticordClient:

    """
    This class is used to make it much easier to use the Boticord API.

    Parameters
    ----------
        bot : :class:`commands.Bot` | :class:`commands.AutoShardedBot`
            The discord.py Bot instance
        token : :class:`str`
            boticord api key

    Attributes
    ----------
        Bots : :class:`modules.bots.Bots`
            :class:`modules.bots.Bots` with all arguments filled.
        Servers : :class:`modules.servers.Servers`
           :class:`modules.servers.Servers` with all arguments filled.
        Users : :class:`modules.users.Users`
            :class:`modules.users.Users` with all arguments filled.
    """

    __slots__ = (
        "Bots",
        "Servers",
        "Users",
        "bot"
    )

    bot: Union[commands.Bot, commands.AutoShardedBot]

    def __init__(self, bot, token=None, **kwargs):
        loop = kwargs.get('loop') or asyncio.get_event_loop()
        session = kwargs.get('session') or aiohttp.ClientSession(loop=loop)
        self.bot = bot
        self.Bots = Bots(bot, token=token, loop=loop, session=session)
        self.Servers = Servers(bot, token=token, loop=loop, session=session)
        self.Users = Users(token=token, loop=loop, session=session)

    def start_loop(self, sleep_time: int = None) -> None:
        """

        Parameters
        ----------
            sleep_time: :class:`int`
                loop sleep time - can be unfilled or None

        """
        self.bot.loop.create_task(self.__loop(sleep_time=sleep_time))

    async def __loop(self, sleep_time: int = None) -> None:
        """
        The internal loop used for automatically posting stats
        """
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            data_to_send = {"servers": len(self.bot.guilds), "users": len(self.bot.users)}

            if isinstance(self.bot, commands.AutoShardedBot):
                data_to_send["shards"] = self.bot.shard_count

            await self.Bots.postStats(data_to_send)

            if sleep_time is None:
                sleep_time = 900

            await asyncio.sleep(sleep_time)
