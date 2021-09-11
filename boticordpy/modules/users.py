import json

from aiohttp import ClientResponse
from typing import Union
import aiohttp
import asyncio

from ..config import Config


async def _json_or_text(response: ClientResponse) -> Union[dict, str]:
    text = await response.text()
    if response.headers['Content-Type'] == 'application/json; charset=utf-8':
        return json.loads(text)
    return text


class Users:

    """
    Class with methods to work with Boticord API Users.
    """

    def __init__(self, **kwargs):
        self.token = kwargs.get('token')
        self.loop = kwargs.get('loop') or asyncio.get_event_loop()
        self.session = kwargs.get('session') or aiohttp.ClientSession(loop=self.loop)

    async def getUserInfo(self, userID: int):
        """
        Returns information about discord user with the given ID.

        Parameters
        ----------
            userID : :class:`int`
                Discord User's ID
        """
        headers = {"Authorization": self.token}

        async with self.session.get(f'{Config.general_api}/profile/{userID}', headers=headers) as resp:
            data = await _json_or_text(resp)
            status = Config.http_exceptions.get(resp.status)
            if status is not None:
                raise status(resp)
            return data

    async def getUserComments(self, userID: int):
        """
        Returns comments of discord user with the given ID.

        Parameters
        ----------
            userID : :class:`int`
                Discord User's ID
        """
        headers = {"Authorization": self.token}

        async with self.session.get(f'{Config.general_api}/profile/{userID}/comments', headers=headers) as resp:
            data = await _json_or_text(resp)
            status = Config.http_exceptions.get(resp.status)
            if status is not None:
                raise status(resp)
            return data

    async def getUserBots(self, userID: int):
        """
        Returns bots of discord user with the given ID.

        Parameters
        ----------
            userID : :class:`int`
                Discord User's ID
        """
        headers = {"Authorization": self.token}

        async with self.session.get(f'{Config.general_api}/bots/{userID}', headers=headers) as resp:
            data = await _json_or_text(resp)
            status = Config.http_exceptions.get(resp.status)
            if status is not None:
                raise status(resp)
            return data
