import aiohttp
import asyncio
from typing import Union
import json
from aiohttp import ClientResponse
from .. import exceptions
from ..config import Config


async def _json_or_text(response: ClientResponse) -> Union[dict, str]:
    text = await response.text()
    if response.headers['Content-Type'] == 'application/json; charset=utf-8':
        return json.loads(text)
    return text


class Servers:
    def __init__(self, bot, **kwargs):
        self.bot = bot
        self.token = kwargs.get('token')
        self.loop = kwargs.get('loop') or asyncio.get_event_loop()
        self.session = kwargs.get('session') or aiohttp.ClientSession(loop=self.loop)

    async def getServerInfo(self, serverID: int):
        """Get Boticord Server info"""
        headers = {}
        async with self.session.get(f'{Config.general_api}/server/{serverID}', headers=headers) as resp:
            data = await _json_or_text(resp)
            if resp.status == 403:
                raise exceptions.Forbidden(resp, data)
            elif resp.status == 401:
                raise exceptions.Unauthorized(resp, data)
            elif resp.status == 404:
                raise exceptions.NotFound(resp, data)
            else:
                return data

    async def getServerComments(self, serverID: int):
        """Get Boticord Server Comments"""
        headers = {}
        async with self.session.get(f'{Config.general_api}/server/{serverID}/comments', headers=headers) as resp:
            data = await _json_or_text(resp)
            if resp.status == 403:
                raise exceptions.Forbidden(resp, data)
            elif resp.status == 401:
                raise exceptions.Unauthorized(resp, data)
            elif resp.status == 404:
                raise exceptions.NotFound(resp, data)
            else:
                return data