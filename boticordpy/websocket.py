# Copyright Marakarka (Viktor K) 2021 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

import logging
import json
import asyncio
import typing

import aiohttp

_logger = logging.getLogger("boticord.websocket")


class BotiCordWebsocket:
    """Represents a client that can be used to interact with the BotiCord by websocket connection."""

    def __init__(self, token: str):
        self.__session = None
        self.loop = asyncio.get_event_loop()
        self.ws = None
        self._listeners = {}
        self.not_closed = False
        self._token = token

    def listener(self):
        """Decorator to set the listener.

        .. warning::

            Callback functions must be a **coroutine**. If they aren't, then you might get unexpected
            errors. In order to turn a function into a coroutine they must be ``async def``
            functions.

        For example:

        .. code-block:: python

            @websocket.listener()
            async def comment_removed(data):
                pass
        """

        def inner(func):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError(f"<{func.__qualname__}> must be a coroutine function")
            self._listeners[func.__qualname__] = func
            _logger.debug(f"Listener {func.__qualname__} added successfully!")
            return func

        return inner

    def register_listener(self, notification_type: str, callback: typing.Any):
        """Method to set the listener.

        Args:
            notify_type (:obj:`str`)
                Type of notification (Check reference page)
            callback (:obj:`function`)
                Coroutine Callback Function

        .. warning::

            Callback functions must be a **coroutine**. If they aren't, then you might get unexpected
            errors. In order to turn a function into a coroutine they must be ``async def``
            functions.
        """
        if not asyncio.iscoroutinefunction(callback):
            raise TypeError(f"<{callback.__qualname__}> must be a coroutine function")

        self._listeners[notification_type] = callback
        _logger.debug(f"Listener {callback.__qualname__} added successfully!")
        return self

    async def connect(self) -> None:
        """Connect to BotiCord."""
        try:
            self.__session = aiohttp.ClientSession()
            self.ws = await self.__session.ws_connect(
                "wss://gateway.boticord.top/websocket/",
                timeout=30.0,
            )

            _logger.info("Connected to BotiCord.")

            self.not_closed = True

            self.loop.create_task(self._receive())
            await self._send_identify()
        except Exception as exc:
            _logger.error("Connecting failed!")

            raise exc

    async def _send_identify(self) -> None:
        await self.ws.send_json({"event": "auth", "data": {"token": self._token}})

    async def _receive(self) -> None:
        while self.not_closed:
            async for msg in self.ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    await self._handle_data(msg.data)
                else:
                    raise RuntimeError

            close_code = self.ws.close_code

            if close_code is not None:
                await self._handle_close(close_code)

    async def _handle_data(self, data):
        data = json.loads(data)

        if data["event"] == "hello":
            _logger.info("Authorized successfully.")
            self.loop.create_task(self._send_ping())
        elif data["event"] == "notify":
            listener = self._listeners.get(data["data"]["type"])
            if listener:
                self.loop.create_task(listener(data["data"]))
        elif data["event"] == "pong":
            _logger.info("Received pong-response.")
            self.loop.create_task(self._send_ping())
        else:
            _logger.error("An error has occurred.")

    async def _handle_close(self, code: int) -> None:
        self.not_closed = False
        await self.__session.close()

        if code == 4000:
            _logger.info("Closed connection successfully.")
            return
        elif code == 1006:
            _logger.error("Token is invalid.")
            return

        _logger.info("Disconnected from BotiCord. Reconnecting...")

        await self.connect()

    async def _send_ping(self) -> None:
        if self.not_closed:
            await asyncio.sleep(45)
            await self.ws.send_json({"event": "ping"})

    async def close(self) -> None:
        """Close websocket connection with BotiCord"""
        if self.ws:
            self.not_closed = False
            await self.ws.close(code=4000)
