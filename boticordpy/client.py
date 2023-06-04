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
            bot_id (Union[:obj:`str`, :obj:`int`])
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

    def autopost(self) -> AutoPost:
        """Returns a helper instance for auto-posting.

        Returns:
            :obj:`~.autopost.AutoPost`: An instance of AutoPost.
        """
        if self._autopost is not None:
            return self._autopost

        self._autopost = AutoPost(self)
        return self._autopost
