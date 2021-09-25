import asyncio

import aiohttp

from ..config import Config, _json_or_text


class Users:

    """
    Class with methods to work with Boticord API Users.
    """

    def __init__(self, **kwargs):
        self.token = kwargs.get('token')
        self.loop = kwargs.get('loop') or asyncio.get_event_loop()
        self.session = kwargs.get('session') or aiohttp.ClientSession(loop=self.loop)

    async def get_user(self, user_id: int):
        """
        Returns information about discord user with the given ID.

        Parameters
        ----------
            user_id : :class:`int`
                Discord User's ID
        """
        headers = {"Authorization": self.token}

        async with self.session.get(f'{Config.general_api}/profile/{user_id}', headers=headers) as resp:
            data = await _json_or_text(resp)
            status = Config.http_exceptions.get(resp.status)
            if status is not None:
                raise status(resp)
            return data

    async def get_user_comments(self, user_id: int):
        """
        Returns comments of discord user with the given ID.

        Parameters
        ----------
            user_id : :class:`int`
                Discord User's ID
        """
        headers = {"Authorization": self.token}

        async with self.session.get(f'{Config.general_api}/profile/{user_id}/comments', headers=headers) as resp:
            data = await _json_or_text(resp)
            status = Config.http_exceptions.get(resp.status)
            if status is not None:
                raise status(resp)
            return data

    async def get_user_bots(self, user_id: int):
        """
        Returns bots of discord user with the given ID.

        Parameters
        ----------
            user_id : :class:`int`
                Discord User's ID
        """
        headers = {"Authorization": self.token}

        async with self.session.get(f'{Config.general_api}/bots/{user_id}', headers=headers) as resp:
            data = await _json_or_text(resp)
            status = Config.http_exceptions.get(resp.status)
            if status is not None:
                raise status(resp)
            return data
