from aiohttp import web
import aiohttp
from discord.ext.commands import Bot, AutoShardedBot

import sys

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

from aiohttp.web_urldispatcher import _WebHandler
from typing import Dict, Union

from . import BoticordClient
from . import config


class _Webhook(TypedDict):
    route: str
    hook_key: str
    func: "_WebHandler"


class BoticordWebhook:
    """
    This class is used as a manager for the Boticord webhook.

    Parameters
    ----------
        bot :class:`commands.Bot` | :class:`commands.AutoShardedBot`
            The discord.py Bot instance
    """

    __app: web.Application
    _webhooks: Dict[
        str,
        _Webhook,
    ]
    _webserver: web.TCPSite

    def __init__(self, bot: Union[Bot, AutoShardedBot], boticord_client: BoticordClient):
        self.bot = bot
        self.boticord_client = boticord_client
        self._webhooks = {}
        self.__app = web.Application()

    def bot_webhook(self, route: str = "/bot", hook_key: str = "") -> "BoticordWebhook":
        """This method may be used to configure the route of boticord bot's webhook.

        Parameters
        ----------
            route :class:`str`
                Bot's webhook route. Must start with ``/``. Defaults - ``/bot``.
            hook_key :class:`str`
                Webhook authorization key.

        Returns
        ----------
            :class:`BoticordWebhook`
        """
        self._webhooks["bot"] = _Webhook(
            route=route or "/bot",
            hook_key=hook_key or "",
            func=self._bot_webhook_interaction_handler,
        )

        return self

    async def _bot_webhook_interaction_handler(self, request: aiohttp.web.Request) -> web.Response:

        auth = request.headers.get("X-Hook-Key")

        if auth == self._webhooks["bot"]["hook_key"]:

            data = await request.json()

            event_in_config = config.Config.events_list.get(data["type"])

            if event_in_config is not None:
                data_for_event = event_in_config(data)
            else:
                data_for_event = data

            try:
                await self.boticord_client.events[data["type"]](data_for_event)
            except:
                pass

            return web.Response(status=200)

        return web.Response(status=401)

    async def _run(self, port: int):
        for webhook in self._webhooks.values():
            self.__app.router.add_post(webhook["route"], webhook["func"])

        runner = web.AppRunner(self.__app)

        await runner.setup()
        self._webserver = web.TCPSite(runner, "0.0.0.0", port)
        await self._webserver.start()

    def run(self, port: int):
        """Runs the webhook.

        Parameters
        ----------
            port
                The port to run the webhook on.
        """
        self.bot.loop.create_task(self._run(port))

    async def close(self) -> None:
        """Stops the webhook."""
        await self._webserver.stop()
