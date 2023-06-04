import asyncio
import typing

import aiohttp

from . import exceptions
from .types import LinkDomain


class HttpClient:
    """
    Represents an HTTP client sending HTTP requests to the BotiCord API.

    Args:
        token (:obj:`str`)
            Your bot's BotiCord API Token.

    Keyword Arguments:
        session: `aiohttp session`_
            The `aiohttp session`_ used for requests to the API.
        loop: `asyncio loop`
    """

    def __init__(self, auth_token: str = None, version: int = 3, **kwargs):
        self.token = auth_token
        self.API_URL = f"https://api.arbuz.pro/"

        loop = kwargs.get("loop") or asyncio.get_event_loop()

        self.session = kwargs.get("session") or aiohttp.ClientSession(loop=loop)

    async def make_request(self, method: str, endpoint: str, **kwargs):
        """Send requests to the API"""

        kwargs["headers"] = {"Content-Type": "application/json"}

        if self.token is not None:
            kwargs["headers"]["Authorization"] = self.token

        url = f"{self.API_URL}{endpoint}"

        async with self.session.request(method, url, **kwargs) as response:
            data = await response.json()

            if response.status == 200 or response.status == 201:
                return data["result"]
            else:
                raise exceptions.HTTPException(
                    {"status": response.status, "error": data["errors"][0]["code"]}
                )

    def get_bot_info(self, bot_id: typing.Union[str, int]):
        """Get information about the specified bot"""
        return self.make_request("GET", f"bots/{bot_id}")

    def post_bot_stats(self, bot_id: typing.Union[str, int], stats: dict):
        """Post bot's stats"""
        return self.make_request("POST", f"bots/{bot_id}/stats", json=stats)

    def get_server_info(self, server_id: int):
        """Get information about specified server"""
        return self.make_request("GET", f"server/{server_id}")

    def get_server_comments(self, server_id: int):
        """Get list of specified server comments"""
        return self.make_request("GET", f"server/{server_id}/comments")

    def post_server_stats(self, payload: dict):
        """Post server's stats"""
        return self.make_request("POST", "server", json=payload)

    def get_user_info(self, user_id: int):
        """Get information about the user"""
        return self.make_request("GET", f"profile/{user_id}")

    def get_user_comments(self, user_id: int):
        """Get specified user's comments"""
        return self.make_request("GET", f"user/{user_id}/comments")

    def get_user_bots(self, user_id: int):
        """Get bots of specified user"""
        return self.make_request("GET", f"bots/{user_id}")

    def get_my_shorted_links(self, code: str = None):
        """Get shorted links of an authorized user"""
        body = {"code": code} if code is not None else {}

        return self.make_request("POST", "links/get", json=body)

    def create_shorted_link(self, code: str, link: str, *, domain: LinkDomain = 1):
        """Create new shorted link"""
        return self.make_request(
            "POST",
            "links/create",
            json={"code": code, "link": link, "domain": int(domain)},
        )

    def delete_shorted_link(self, code: str, domain: LinkDomain = 1):
        """Delete shorted link"""
        return self.make_request(
            "POST", "links/delete", json={"code": code, "domain": int(domain)}
        )
