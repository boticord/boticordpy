import asyncio

import aiohttp
import discord
from discord.ext import commands

from types import Union

from .modules import bots, servers, users


class BoticordClient:
    __slots__ = (
        "Bots",
        "Servers",
        "Users"
    )

    bot: Union[discord.Client, discord.AutoShardedClient, commands.Bot, commands.AutoShardedBot]

    def __init__(self, bot, **kwargs):
        token = kwargs.get('token')
        loop = kwargs.get('loop') or asyncio.get_event_loop()
        session = kwargs.get('session') or aiohttp.ClientSession(loop=loop)
        self.Bots = bots.Bots(bot, token=token, loop=loop, session=session)
        self.Servers = servers.Servers(bot, token=token, loop=loop, session=session)
        self.Users = users.Users(bot, token=token, loop=loop, session=session)