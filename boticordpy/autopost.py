import asyncio
import typing

from . import exceptions as bexc


class AutoPost:
    __slots__ = (
        "client",
        "_interval",
        "_success",
        "_error",
        "_stats",
        "_task",
        "_stopped"
    )

    _success: typing.Any
    _error: typing.Any
    _stats: typing.Any
    _task: typing.Optional["asyncio.Task[None]"]

    def __init__(self, client):
        self.client = client
        self._stopped: bool = False
        self._interval: int = 900
        self._task: typing.Optional["asyncio.Task[None]"] = None

    @property
    def is_running(self) -> bool:
        return self._task is not None and not self._task.done()

    def on_success(self, callback: typing.Any = None):
        if callback is not None:
            self._success = callback
            return self

        def inner(func):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError(f"<{func.__qualname__}> must be a coroutine function")

            self._success = callback
            return func

        return inner

    def on_error(self, callback: typing.Any = None):
        if callback is not None:
            self._error = callback
            return self

        def inner(func):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError(f"<{func.__qualname__}> must be a coroutine function")

            self._error = callback
            return func

        return inner

    def init_stats(self, callback: typing.Any = None):
        if callback is not None:
            self._stats = callback
            return self

        def inner(func):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError(f"<{func.__qualname__}> must be a coroutine function")

            self._stats = callback
            return func

        return inner

    @property
    def interval(self) -> float:
        return self._interval

    def set_interval(self, seconds: int) -> "AutoPost":
        if seconds < 900:
            raise ValueError("no. Boticord recommends not to set interval lower than 900 seconds!")

        self._interval = seconds
        return self

    async def _internal_loop(self) -> None:
        while True:
            stats = await self._stats()
            try:
                await self.client.http.post_bot_stats(stats)
            except Exception as err:
                on_error = getattr(self, "_error", None)
                if on_error:
                    await on_error(err)
            else:
                on_success = getattr(self, "_success", None)
                if on_success:
                    await on_success()

            if self._stopped:
                return None

            await asyncio.sleep(self._interval)

    def start(self):
        if not hasattr(self, "_stats"):
            raise bexc.InternalException("You must provide stats")

        if self.is_running:
            raise bexc.InternalException("Automatically stats posting is already running")

        task = asyncio.ensure_future(self._internal_loop())
        self._task = task
        return task

    def stop(self) -> None:
        if not self.is_running:
            return None

        self._stopped = True
