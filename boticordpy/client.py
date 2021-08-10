from discord.ext import commands
from typing import Union
import asyncio
import aiohttp

import modules


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
        "Users"
    )

    bot: Union[commands.Bot, commands.AutoShardedBot]

    def __init__(self, bot, token=None, **kwargs):
        loop = kwargs.get('loop') or asyncio.get_event_loop()
        session = kwargs.get('session') or aiohttp.ClientSession(loop=loop)
        self.Bots = modules.Bots(bot, token=token, loop=loop, session=session)
        self.Servers = modules.Servers(bot, token=token, loop=loop, session=session)
        self.Users = modules.Users(token=token, loop=loop, session=session)