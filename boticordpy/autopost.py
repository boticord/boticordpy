import asyncio
import typing
import logging

from . import exceptions as bexc

_logger = logging.getLogger("boticord.autopost")


class AutoPost:
    """
    You can use this to post stats automatically.

    Args:
        client (:obj:`~.client.BoticordClient`)
            An instance of BoticordClient.
    """

    __slots__ = (
        "client",
        "_interval",
        "_success",
        "_error",
        "_stats",
        "_task",
        "_stopped",
        "bot_id"
    )

    _success: typing.Any
    _error: typing.Any
    _stats: typing.Any
    _task: typing.Optional["asyncio.Task[None]"]

    bot_id: str

    def __init__(self, client):
        self.client = client
        self._stopped: bool = False
        self._interval: int = 900
        self._task: typing.Optional["asyncio.Task[None]"] = None

        self.bot_id = None

    @property
    def is_running(self) -> bool:
        """
        Is autopost running?
        """
        return self._task is not None and not self._task.done()

    def on_success(self, callback: typing.Any = None):
        """
        Registers success callback.

        .. warning::

            Callback functions must be a **coroutine**. If they aren't, then you might get unexpected
            errors. In order to turn a function into a coroutine they must be ``async def``
            functions.

        This method can be used as a decorator (if you want).
        """

        if callback is not None:
            self._success = callback
            return self

        def inner(func):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError(f"<{func.__qualname__}> must be a coroutine function")

            self._success = callback
            return func

        _logger.info("Registering success callback")

        return inner

    def on_error(self, callback: typing.Any = None):
        """
        Registers error callback.

        .. warning::

            Callback functions must be a **coroutine**. If they aren't, then you might get unexpected
            errors. In order to turn a function into a coroutine they must be ``async def``
            functions.

        The callback function requires to take Exception argument.
        This method can be used as a decorator (if you want).
        """
        if callback is not None:
            self._error = callback
            return self

        def inner(func):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError(f"<{func.__qualname__}> must be a coroutine function")

            self._error = callback
            return func

        _logger.info("Registering error callback")

        return inner

    def init_stats(self, callback: typing.Any = None):
        """
        Registers a function that will return stats. Registered Function Must return dictionary.

        .. warning::

            None of the values must be equal to 0. Specify None instead of 0.

        .. warning::

            Callback functions must be a **coroutine**. If they aren't, then you might get unexpected
            errors. In order to turn a function into a coroutine they must be ``async def``
            functions.

        This method can be used as a decorator (if you want).
        """
        if callback is not None:
            self._stats = callback
            return self

        def inner(func):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError(f"<{func.__qualname__}> must be a coroutine function")

            self._stats = callback
            return func

        _logger.info("Registered stats initialization function")

        return inner

    @property
    def interval(self) -> float:
        """The interval between posting stats."""
        return self._interval

    def set_interval(self, seconds: int) -> "AutoPost":
        """
        Sets the interval between posting stats.
        
        Args:
            seconds (:obj:`int`)
                The interval.
        Raises:
            :obj:`ValueError`
                Boticord recommends not to set interval lower than 900 seconds!
        """
        if seconds < 900:
            raise ValueError(
                "no. Boticord recommends not to set interval lower than 900 seconds!"
            )

        self._interval = seconds
        return self

    async def _internal_loop(self) -> None:
        while True:
            stats = await self._stats()
            try:
                await self.client.http.post_bot_stats(self.bot_id, stats)
                _logger.info("Tried to post bot stats")
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

    def start(self, bot_id: typing.Union[str, int]):
        """
        Starts the loop.

        Args:
            bot_id ( Union[:obj:`int`, :obj:`str`] )
                Id of the bot to send stats of.

        Raises:
            :obj:`~.exceptions.InternalException`
                If there's no callback (for getting stats) provided or the autopost is already running.
        """

        self.bot_id = bot_id

        if not hasattr(self, "_stats"):
            raise bexc.InternalException("You must provide stats")

        if self.is_running:
            raise bexc.InternalException(
                "Automatically stats posting is already running"
            )

        task = asyncio.ensure_future(self._internal_loop())
        self._task = task

        _logger.info("Started autoposting")

        return task

    def stop(self) -> None:
        """
        Stops the autopost.
        """
        if not self.is_running:
            return None

        self._stopped = True

        _logger.info("Stopped autoposting")
