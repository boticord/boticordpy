class BoticordException(Exception):
    """Base exception class for boticordpy.
    This could be caught to handle any exceptions thrown from this library.
    """


class HTTPException(BoticordException):
    """Exception that's thrown when an HTTP request operation fails.

    Attributes
    ----------
    response:
        The response of the failed HTTP request.
    message:
        The text of the error. Could be an empty string.
    """

    def __init__(self, response):
        self.response = response

        fmt = f"{self.response.reason} (Status code: {self.response.status})"

        super().__init__(fmt)


class Unauthorized(HTTPException):
    """Exception that's thrown when status code 401 occurs."""


class Forbidden(HTTPException):
    """Exception that's thrown when status code 403 occurs."""


class NotFound(HTTPException):
    """Exception that's thrown when status code 404 occurs."""


class ToManyRequests(HTTPException):
    """Exception that's thrown when status code 429 occurs."""


class ServerError(HTTPException):
    """Exception that's thrown when status code 500 or 503 occurs."""
