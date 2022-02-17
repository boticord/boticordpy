import asyncio

import aiohttp

from . import exceptions


class HttpClient:
    """
    Represents an HTTP client sending HTTP requests to the Top.gg API.

    Args:
        token (:obj:`str`)
            Your bot's Boticord API Token.

    Keyword Arguments:
        session: `aiohttp session`_
            The `aiohttp session`_ used for requests to the API.
        loop: `asyncio loop`
    """

    def __init__(self, auth_token, **kwargs):
        self.token = auth_token
        self.API_URL = "https://api.boticord.top/v1/"

        loop = kwargs.get('loop') or asyncio.get_event_loop()

        self.session = kwargs.get('session') or aiohttp.ClientSession(loop=loop)

    async def make_request(self,
                           method: str,
                           endpoint: str,
                           **kwargs):
        """Send requests to the API"""

        kwargs["headers"] = {
            "Content-Type": "application/json",
            "Authorization": self.token
        }

        url = f"{self.API_URL}{endpoint}"

        async with self.session.request(method,
                                        url,
                                        **kwargs) as response:
            data = await response.json()

            if response.status == 200:
                return data
            elif response.status == 401:
                raise exceptions.Unauthorized(response)
            elif response.status == 403:
                raise exceptions.Forbidden(response)
            elif response.status == 404:
                raise exceptions.NotFound(response)
            elif response.status == 429:
                raise exceptions.ToManyRequests(response)
            elif response.status == 500:
                raise exceptions.ServerError(response)
            elif response.status == 503:
                raise exceptions.ServerError(response)

        raise exceptions.HTTPException(response)

    def get_bot_info(self, bot_id: int):
        """Get information about the specified bot"""
        return self.make_request("GET", f"bot/{bot_id}")

    def get_bot_comments(self, bot_id: int):
        """Get list of specified bot comments"""
        return self.make_request("GET", f"bot/{bot_id}/comments")

    def post_bot_stats(self, stats: dict):
        """Post bot's stats"""
        return self.make_request("POST", "stats", json=stats)

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
