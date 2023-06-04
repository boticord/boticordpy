import typing

from . import types as boticord_types
from .http import HttpClient
from .autopost import AutoPost


class BoticordClient:
    """Represents a client that can be used to interact with the BotiCord API.

    Note:
        Remember that every http method can return an http exception.

    Args:
        token (:obj:`str`)
            Your bot's Boticord API Token.
        version (:obj:`int`)
            BotiCord API version (Default: 3)
    """

    __slots__ = ("http", "_autopost", "_token")

    http: HttpClient

    def __init__(self, token: str = None, version: int = 3):
        self._token = token
        self._autopost: typing.Optional[AutoPost] = None
        self.http = HttpClient(token, version)

    async def get_bot_info(
        self, bot_id: typing.Union[str, int]
    ) -> boticord_types.ResourceBot:
        """Gets information about specified bot.

        Args:
            bot_id (Union[:obj:`str`, :obj:`int`])
                Id of the bot

        Returns:
            :obj:`~.types.ResourceBot`:
                ResourceBot object.
        """
        response = await self.http.get_bot_info(bot_id)
        return boticord_types.ResourceBot.from_dict(response)

    async def post_bot_stats(
        self,
        bot_id: typing.Union[str, int],
        *,
        servers: int = 0,
        shards: int = 0,
        users: int = 0,
    ) -> boticord_types.ResourceBot:
        """Post Bot's stats.

        Args:
            bot_id (Union[:obj:`str`, :obj:`)
                Id of the bot to post stats of.
            servers ( :obj:`int` )
                Bot's servers count
            shards ( :obj:`int` )
                Bot's shards count
            users ( :obj:`int` )
                Bot's users count
        Returns:
            :obj:`~.types.ResourceBot`:
                ResourceBot object.
        """
        response = await self.http.post_bot_stats(
            bot_id, {"servers": servers, "shards": shards, "users": users}
        )
        return boticord_types.ResourceBot.from_dict(response)

    async def get_server_info(self, server_id: int):
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
        Payload is raw, because if you use it - you know what you are doing.
        You can find more information about payload `in BotiCord API Docs <https://docs.boticord.top/methods/servers/>`_

        Args:
            payload (:obj:`dict`)
                Custom data (Use Boticord API docs.)
        Returns:
            :obj:`dict`:
                Boticord API Response.
        """
        response = await self.http.post_server_stats(payload)
        return response

    async def get_user_info(self, user_id: int):
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

    async def get_user_comments(self, user_id: int):
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

    async def get_my_shorted_links(self, *, code: str = None):
        """Gets shorted links of an authorized user

        Args:
            code (:obj:`str`)
                Code of shorted link. Could be None.

        Returns:
            Union[:obj:`list` [ :obj:`~.types.ShortedLink` ], :obj:`~types.ShortedLink`]:
                List of shorted links if none else shorted link
        """
        response = await self.http.get_my_shorted_links(code)

        return (
            [boticord_types.ShortedLink(**link) for link in response]
            if code is None
            else boticord_types.ShortedLink(**response[0])
        )

    async def create_shorted_link(self, *, code: str, link: str, domain=1):
        """Creates new shorted link

        Args:
            code (:obj:`str`)
                Code of link to short.
            link (:obj:`str`)
                Link to short.
            domain (:obj:`~.types.LinkDomain`)
                Domain to use in shorted link

        Returns:
            :obj:`~types.ShortedLink`:
                Shorted Link
        """
        response = await self.http.create_shorted_link(code, link, domain=domain)

        return boticord_types.ShortedLink(**response)

    async def delete_shorted_link(self, code: str, domain=1):
        """Deletes shorted link

        Args:
            code (:obj:`str`)
                Code of link to delete.
            domain (:obj:`~.types.LinkDomain`)
                Domain that is used in shorted link

        Returns:
            :obj:`bool`:
                Is link deleted successfully?
        """
        response = await self.http.delete_shorted_link(code, domain)

        return response.get("ok", False)

    def autopost(self) -> AutoPost:
        """Returns a helper instance for auto-posting.

        Returns:
            :obj:`~.autopost.AutoPost`: An instance of AutoPost.
        """
        if self._autopost is not None:
            return self._autopost

        self._autopost = AutoPost(self)
        return self._autopost
