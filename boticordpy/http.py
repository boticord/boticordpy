import asyncio

import aiohttp

from . import exceptions


class HttpClient:
    def __init__(self, auth_token, **kwargs):
        self.token = auth_token
        self.API_URL = "https://api.boticord.top/v1/"

        loop = kwargs.get('loop') or asyncio.get_event_loop()

        self.session = kwargs.get('session') or aiohttp.ClientSession(loop=loop)

    async def make_request(self,
                           method: str,
                           endpoint: str,
                           **kwargs):
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
        return self.make_request("GET", f"bot/{bot_id}")

    def get_bot_comments(self, bot_id: int):
        return self.make_request("GET", f"bot/{bot_id}/comments")

    def post_bot_stats(self, stats: dict):
        return self.make_request("POST", "stats", json=stats)

    def get_server_info(self, server_id: int):
        return self.make_request("GET", f"server/{server_id}")

    def get_server_comments(self, server_id: int):
        return self.make_request("GET", f"server/{server_id}/comments")

    def post_server_stats(self, payload: dict):
        return self.make_request("POST", "server", json=payload)

    def get_user_info(self, user_id: int):
        return self.make_request("GET", f"profile/{user_id}")

    def get_user_comments(self, user_id: int):
        return self.make_request("GET", f"user/{user_id}/comments")

    def get_user_bots(self, user_id: int):
        return self.make_request("GET", f"bots/{user_id}")
