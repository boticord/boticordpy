import typing
import logging

from . import types as boticord_types
from .http import HttpClient
from .autopost import AutoPost
from .exceptions import MeilisearchException

_logger = logging.getLogger("boticord")


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

    __slots__ = ("http", "_autopost", "_token", "_meilisearch_api_key")

    http: HttpClient

    def __init__(self, token: str = None, version: int = 3):
        self._token = token
        self._meilisearch_api_key = None
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
        _logger.info("Requesting information about bot")

        response = await self.http.get_bot_info(bot_id)
        return boticord_types.ResourceBot.from_dict(response)

    async def post_bot_stats(
        self,
        bot_id: typing.Union[str, int],
        *,
        servers: typing.Optional[int] = None,
        shards: typing.Optional[int] = None,
        users: typing.Optional[int] = None,
    ) -> boticord_types.ResourceBot:
        """Post Bot's stats.

        .. warning::

            None of the values must be equal to 0. Specify None instead of 0.

        Args:
            bot_id (Union[:obj:`str`, :obj:`int`])
                Id of the bot to post stats of.
            servers ( Optional[:obj:`int`] )
                Bot's servers count
            shards ( Optional[:obj:`int`] )
                Bot's shards count
            users ( Optional[:obj:`int`] )
                Bot's users count

        Returns:
            :obj:`~.types.ResourceBot`:
                ResourceBot object.
        """
        _logger.info("Posting bot stats")

        response = await self.http.post_bot_stats(
            bot_id, {"servers": servers, "shards": shards, "members": users}
        )
        return boticord_types.ResourceBot.from_dict(response)

    async def get_server_info(
        self, server_id: typing.Union[str, int]
    ) -> boticord_types.ResourceServer:
        """Gets information about specified server.

        Args:
            server_id (Union[:obj:`str`, :obj:`int`])
                Id of the server

        Returns:
            :obj:`~.types.ResourceServer`:
                ResourceServer object.
        """
        _logger.info("Requesting information about server")

        response = await self.http.get_server_info(server_id)
        return boticord_types.ResourceServer.from_dict(response)

    async def get_user_info(
        self, user_id: typing.Union[str, int]
    ) -> boticord_types.UserProfile:
        """Gets information about specified user.

        Args:
            user_id (Union[:obj:`str`, :obj:`int`])
                Id of the user

        Returns:
            :obj:`~.types.UserProfile`:
                UserProfile object.
        """
        _logger.info("Requesting information about user")

        response = await self.http.get_user_info(user_id)
        return boticord_types.UserProfile.from_dict(response)

    async def __search_for(self, index, data):
        """Search for something on BotiCord"""
        if self._meilisearch_api_key is None:
            token_response = await self.http.get_search_key()
            self._meilisearch_api_key = token_response["key"]

        try:
            response = await self.http.search_for(
                index, self._meilisearch_api_key, data
            )
        except MeilisearchException:
            token_response = await self.http.get_search_key()
            self._meilisearch_api_key = token_response["key"]

            response = await self.http.search_for(
                index, self._meilisearch_api_key, data
            )

        return response["hits"]

    async def search_for_bots(
        self, **kwargs
    ) -> typing.List[boticord_types.MeiliIndexedBot]:
        """Search for bots on BotiCord.

        Note:
            You can find every keyword argument `here <https://www.meilisearch.com/docs/reference/api/search#search-parameters>`_.

        Returns:
            List[:obj:`~.types.MeiliIndexedBot`]:
                List of found bots
        """
        _logger.info("Searching for bots on BotiCord")

        response = await self.__search_for("bots", kwargs)
        return [boticord_types.MeiliIndexedBot.from_dict(bot) for bot in response]

    async def search_for_servers(
        self, **kwargs
    ) -> typing.List[boticord_types.MeiliIndexedServer]:
        """Search for servers on BotiCord.

        Note:
            You can find every keyword argument `here <https://www.meilisearch.com/docs/reference/api/search#search-parameters>`_.

        Returns:
            List[:obj:`~.types.MeiliIndexedServer`]:
                List of found servers
        """
        _logger.info("Searching for servers on BotiCord")

        response = await self.__search_for("servers", kwargs)
        return [
            boticord_types.MeiliIndexedServer.from_dict(server) for server in response
        ]

    async def search_for_comments(
        self, **kwargs
    ) -> typing.List[boticord_types.MeiliIndexedComment]:
        """Search for comments on BotiCord.

        Note:
            You can find every keyword argument `here <https://www.meilisearch.com/docs/reference/api/search#search-parameters>`_.

        Returns:
            List[:obj:`~.types.MeiliIndexedComment`]:
                List of found comments
        """
        _logger.info("Searching for comments on BotiCord")

        response = await self.__search_for("comments", kwargs)
        return [
            boticord_types.MeiliIndexedComment.from_dict(comment)
            for comment in response
        ]

    def autopost(self) -> AutoPost:
        """Returns a helper instance for auto-posting.

        Returns:
            :obj:`~.autopost.AutoPost`: An instance of AutoPost.
        """
        if self._autopost is not None:
            return self._autopost

        self._autopost = AutoPost(self)
        return self._autopost
