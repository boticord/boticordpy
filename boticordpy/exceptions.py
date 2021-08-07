class BoticordException(Exception):
    pass


class HTTPException(BoticordException):
    def __init__(self, response, message):
        self.response = response
        if isinstance(message, dict):
            self.text = message.get('message', '')
            self.code = message.get('code', 0)
        else:
            self.text = message

        fmt = f"{self.response.reason} (Status code: {self.response.status})"
        if self.text:
            fmt = f"{fmt}: {self.text}"

        super().__init__(fmt)


class Unauthorized(HTTPException):
    pass


class NotFound(HTTPException):
    pass


class Forbidden(HTTPException):
    pass
