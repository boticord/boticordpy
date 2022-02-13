import asyncio
import typing

from .types import BumpResponse, CommentResponse

from aiohttp import web
import aiohttp


class Webhook:
    __slots__ = (
        "_webserver",
        "_listeners",
        "_is_running",
        "__app",
        "_endpoint_name",
        "_x_hook_key",
        "_loop"
    )

    __app: web.Application
    _webserver: web.TCPSite

    def __init__(self, x_hook_key: str, endpoint_name: str, **kwargs) -> None:
        self._x_hook_key = x_hook_key
        self._endpoint_name = endpoint_name
        self._listeners = {}
        self.__app = web.Application()
        self._is_running = False
        self._loop = kwargs.get('loop') or asyncio.get_event_loop()

    def listener(self, response_type: str):
        def inner(func):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError(f"<{func.__qualname__}> must be a coroutine function")
            self._listeners[response_type] = func
            return func

        return inner

    def register_listener(self, response_type: str, callback: typing.Any):
        if not asyncio.iscoroutinefunction(callback):
            raise TypeError(f"<{func.__qualname__}> must be a coroutine function")

        self._listeners[response_type] = callback
        return self

    async def _interaction_handler(self, request: aiohttp.web.Request) -> web.Response:
        auth = request.headers.get("X-Hook-Key")

        if auth == self._x_hook_key:
            data = await request.json()

            responder = self._listeners.get(data["type"])

            if responder is not None:
                await responder(
                    (BumpResponse if data["type"].endswith("_bump") else CommentResponse)(**data)
                )

            return web.Response(status=200)

        return web.Response(status=401)

    async def _run(self, port):
        self.__app.router.add_post("/" + self._endpoint_name, self._interaction_handler)

        runner = web.AppRunner(self.__app)
        await runner.setup()

        self._webserver = web.TCPSite(runner, "0.0.0.0", port)
        await self._webserver.start()

        self._is_running = True

    def start(self, port: int) -> None:
        self._loop.create_task(self._run(port))

    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def listeners(self) -> dict:
        return self._listeners

    @property
    def app(self) -> web.Application:
        return self.__app

    async def close(self) -> None:
        await self._webserver.stop()

        self._is_running = False
