import typing

from . import types as boticord_types
from .http import HttpClient
from .autopost import AutoPost


class BoticordClient:
    """Represents a client that can be used to interact with the BotiCord API.

    Note:
        Remember that every http method can return http exception.

    Args:
        token (:obj:`str`)
            Your bot's Boticord API Token.
    """
    __slots__ = (
        "http",
        "_autopost",
        "_token"
    )

    http: HttpClient

    def __init__(self, token=None):
        self._token = token
        self._autopost: typing.Optional[AutoPost] = None
        self.http = HttpClient(token)

    async def get_bot_info(self, bot_id: int) -> boticord_types.Bot:
        """Gets information about specified bot.

        Args:
            bot_id (:obj:`int`)
                Id of the bot

        Returns:
            :obj:`~.types.Bot`:
                Bot object.
        """
        response = await self.http.get_bot_info(bot_id)
        return boticord_types.Bot(**response)

    async def get_bot_comments(self, bot_id: int) -> list:
        """Gets list of comments of specified bot.

        Args:
            bot_id (:obj:`int`)
                Id of the bot

        Returns:
            :obj:`list` [ :obj:`~.types.SingleComment` ]:
                List of comments.
        """
        response = await self.http.get_bot_comments(bot_id)
        return [boticord_types.SingleComment(**comment) for comment in response]

    async def post_bot_stats(self, servers: int = 0, shards: int = 0, users: int = 0) -> dict:
        """Post Bot's stats.

        Args:
            servers ( :obj:`int` )
                Bot's servers count
            shards ( :obj:`int` )
                Bot's shards count
            users ( :obj:`int` )
                Bot's users count
        Returns:
            :obj:`dict`:
                Boticord API Response status
        """
        response = await self.http.post_bot_stats({
            "servers": servers,
            "shards": shards,
            "users": users
        })
        return response

    async def get_server_info(self, server_id: int) -> boticord_types.Server:
        """Gets information about specified server.

        Args:
            server_id (:obj:`int`)
                Id of the server

        Returns:
            :obj:`~.types.Server`:
                Server object.
        """
        response = await self.http.get_server_info(server_id)
        return boticord_types.Server(**response)

    async def get_server_comments(self, server_id: int) -> list:
        """Gets list of comments of specified server.

        Args:
            server_id (:obj:`int`)
                Id of the server

        Returns:
            :obj:`list` [ :obj:`~.types.SingleComment` ]:
                List of comments.
        """
        response = await self.http.get_server_comments(server_id)
        return [boticord_types.SingleComment(**comment) for comment in response]

    async def post_server_stats(self, payload: dict) -> dict:
        """Post Server's stats. You must be Boticord-Service bot.

        Args:
            payload (:obj:`dict`)
                Custom data (Use Boticord API docs.)
        Returns:
            :obj:`dict`:
                Boticord API Response.
        """
        response = await self.http.post_server_stats(payload)
        return response

    async def get_user_info(self, user_id: int) -> boticord_types.UserProfile:
        """Gets information about specified user.

        Args:
            user_id (:obj:`int`)
                Id of the user

        Returns:
            :obj:`~.types.UserProfile`:
                User Profile object.
        """
        response = await self.http.get_user_info(user_id)
        return boticord_types.UserProfile(**response)

    async def get_user_comments(self, user_id: int) -> boticord_types.UserComments:
        """Gets comments of specified user.

        Args:
            user_id (:obj:`int`)
                Id of the user

        Returns:
            :obj:`~.types.UserComments`:
                User comments on Bots and Servers pages.
        """
        response = await self.http.get_user_comments(user_id)
        return boticord_types.UserComments(**response)

    async def get_user_bots(self, user_id: int) -> list:
        """Gets list of bots of specified user.

        Args:
            user_id (:obj:`int`)
                Id of the user

        Returns:
            :obj:`list` [ :obj:`~.types.SimpleBot` ]:
                List of simple information about users bots.
        """
        response = await self.http.get_user_bots(user_id)
        return [boticord_types.SimpleBot(**bot) for bot in response]

    def autopost(self) -> AutoPost:
        """Returns a helper instance for auto-posting.

        Returns:
            :obj:`~.autopost.AutoPost`: An instance of AutoPost.
        """
        if self._autopost is not None:
            return self._autopost

        self._autopost = AutoPost(self)
        return self._autopost
