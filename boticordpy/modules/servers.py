import json

from aiohttp import ClientResponse
from typing import Union
import aiohttp
import asyncio
import discord

from ..config import Config


async def _json_or_text(response: ClientResponse) -> Union[dict, str]:
    text = await response.text()
    if response.headers['Content-Type'] == 'application/json; charset=utf-8':
        return json.loads(text)
    return text


class Servers:

    """
    Class with methods to work with Boticord API Servers.

    Parameters
    ----------
        bot : :class:`commands.Bot` | :class:`commands.AutoShardedBot`
            The discord.py Bot instance
    """

    def __init__(self, bot, **kwargs):
        self.bot = bot
        self.token = kwargs.get('token')
        self.loop = kwargs.get('loop') or asyncio.get_event_loop()
        self.session = kwargs.get('session') or aiohttp.ClientSession(loop=self.loop)

    async def getServerInfo(self, serverID: int):
        """
        Returns information about discord server with the given ID.

        Parameters
        ----------
           serverID : :class:`int`
                Discord Server's ID
        """
        headers = {"Authorization": self.token}

        async with self.session.get(f'{Config.general_api}/server/{serverID}', headers=headers) as resp:
            data = await _json_or_text(resp)
            status = Config.http_exceptions.get(resp.status)
            if status is not None:
                raise status(resp)
            return data

    async def getServerComments(self, serverID: int):
        """
        Returns comments of the discord server with the given ID.

        Parameters
        ----------
            serverID : :class:`int`
                Discord Server's ID
        """
        headers = {"Authorization": self.token}

        async with self.session.get(f'{Config.general_api}/server/{serverID}/comments', headers=headers) as resp:
            data = await _json_or_text(resp)
            status = Config.http_exceptions.get(resp.status)
            if status is not None:
                raise status(resp)
            return data

    async def postServerStats(self, message: discord.Message, custom_stats: dict = None):
        """
        Post server stats to Boticord API.

        Parameters
        ----------
            message: :class:`discord.Message`
                Message object of used command.
            custom_stats: :class:`dict`
                Dict with custom server stats. (Optional)
        """
        if not self.token:
            return "Require Authentication"

        if custom_stats is None:
            guild = message.guild
            guild_owner = guild.owner

            stats = {
                "serverID": str(guild.id),
                "up": 1,
                "status": 1,
                "serverName": guild.name,
                "serverAvatar": str(guild.icon_url),
                "serverMembersAllCount": guild.member_count,
                "serverMembersOnlineCount": 0,
                "serverOwnerTag": guild_owner.name + "#" + guild_owner.discriminator,
                "serverOwnerID": str(guild_owner.id)
            }
        else:
            stats = custom_stats

        headers = {"Authorization": self.token}

        async with self.session.post(f'{Config.general_api}/server', headers=headers, json=stats) as resp:
            data = await _json_or_text(resp)
            status = Config.http_exceptions.get(resp.status)
            if status is not None:
                raise status(resp)
            return data
