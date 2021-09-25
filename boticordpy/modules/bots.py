import asyncio

import aiohttp

from ..config import Config, _json_or_text


class Bots:

    """
    Class with methods to work with Boticord API Bots.

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

    async def get_bot_info(self, bot_id: int):
        """
        Returns information about discord bot with the given ID.

        Parameters
        ----------
            bot_id : :class:`int`
                Discord Bot's ID
        """
        headers = {"Authorization": self.token}

        async with self.session.get(f'{Config.general_api}/bot/{bot_id}', headers=headers) as resp:
            data = await _json_or_text(resp)
            status = Config.http_exceptions.get(resp.status)

            if status is not None:
                raise status(resp)
            return data

    async def get_bot_comments(self, bot_id: int):
        """
        Returns comments of the discord bot with the given ID.

        Parameters
        ----------
            bot_id : :class:`int`
                Discord Bot's ID
        """
        headers = {"Authorization": self.token}

        async with self.session.get(f'{Config.general_api}/bot/{bot_id}/comments', headers=headers) as resp:
            data = await _json_or_text(resp)
            status = Config.http_exceptions.get(resp.status)
            if status is not None:
                raise status(resp)
            return data

    async def post_stats(self, stats: dict):
        """
        Post stats to Boticord API.

        Parameters
        ----------
            stats: :class:`dict`
                A dictionary of {``guilds``: :class:`int`, ``shards``: :class:`int`, ``users``: :class:`int`}
        """
        if not self.token:
            return "Require Authentication"

        headers = {"Authorization": self.token}

        async with self.session.post(f'{Config.general_api}/stats', headers=headers, json=stats) as resp:
            data = await _json_or_text(resp)
            status = Config.http_exceptions.get(resp.status)
            if status is not None:
                raise status(resp)
            return data
