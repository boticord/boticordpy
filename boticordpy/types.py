import typing

KT = typing.TypeVar("KT")
VT = typing.TypeVar("VT")


def parse_response_dict(input_data: dict) -> dict:
    data = input_data.copy()

    for key, value in data.copy().items():
        converted_key = "".join(
            ["_" + x.lower() if x.isupper() else x for x in key]
        ).lstrip("_")

        if key != converted_key:
            del data[key]

        data[converted_key] = value

    return data


def parse_with_information_dict(bot_data: dict) -> dict:
    data = bot_data.copy()

    for key, value in data.copy().items():
        if key.lower() == "links":
            converted_key = "page_links"
        else:
            converted_key = "".join(
                ["_" + x.lower() if x.isupper() else x for x in key]
            ).lstrip("_")

        if key != converted_key:
            del data[key]

        if key.lower() == "information":
            for information_key, information_value in value.copy().items():
                converted_information_key = "".join(
                    ["_" + x.lower() if x.isupper() else x for x in information_key]
                ).lstrip("_")

                data[converted_information_key] = information_value

            del data["information"]
        else:
            data[converted_key] = value

    return data


def parse_user_comments_dict(response_data: dict) -> dict:
    data = response_data.copy()

    for key, value in data.copy().items():
        data[key] = [SingleComment(**comment) for comment in value]

    return data


class ApiData(dict, typing.MutableMapping[KT, VT]):
    """Base class used to represent received data from the API.
    """

    def __init__(self, **kwargs: VT) -> None:
        super().__init__(**parse_response_dict(kwargs))
        self.__dict__ = self


class SingleComment(ApiData):
    """This model represents single comment"""

    user_id: str
    """Comment's author Id (`str`)"""

    text: str
    """Comment content"""

    vote: int
    """Comment vote value (`-1,` `0`, `1`)"""

    is_updated: bool
    """Was comment updated?"""

    created_at: int
    """Comment Creation date timestamp"""

    updated_at: int
    """Last edit date timestamp"""

    def __init__(self, **kwargs):
        super().__init__(**parse_response_dict(kwargs))


class Bot(ApiData):
    """This model represents a bot, returned from the Boticord API"""
    id: str
    """Bot's Id"""

    short_code: typing.Optional[str]
    """Bot's page short code"""

    page_links: list
    """List of bot's page urls"""

    server: dict
    """Bot's support server"""

    bumps: int
    """Bumps count"""

    prefix: str
    """How many times users have added the bot?"""

    permissions: int
    """Bot's permissions"""

    tags: list
    """Bot's search-tags"""

    developers: list
    """List of bot's developers Ids"""

    links: typing.Optional[dict]
    """Bot's social medias"""

    library: typing.Optional[str]
    """Bot's library"""

    short_description: typing.Optional[str]
    """Bot's short description"""

    long_description: typing.Optional[str]
    """Bot's long description"""

    badge: typing.Optional[int]
    """Bot's badge"""

    stats: dict
    """Bot's stats"""

    status: str
    """Bot's approval status"""

    def __init__(self, **kwargs):
        super().__init__(**parse_with_information_dict(kwargs))


class Server(ApiData):
    """This model represents a server, returned from the Boticord API"""

    id: str
    """Server's Id"""

    short_code: typing.Optional[str]
    """Server's page short code"""

    status: str
    """Server's approval status"""

    page_links: list
    """List of server's page urls"""

    bot: dict
    """Bot where this server is used for support users"""

    name: str
    """Name of the server"""

    avatar: str
    """Server's avatar"""

    members: list
    """Members counts - `[all, onlinw]`"""

    owner: typing.Optional[str]
    """Server's owner Id"""

    bumps: int
    """Bumps count"""

    tags: list
    """Server's search-tags"""

    links: dict
    """Server's social medias"""

    short_description: typing.Optional[str]
    """Server's short description"""

    long_description: typing.Optional[str]
    """Server's long description"""

    badge: typing.Optional[str]
    """Server's badge"""

    def __init__(self, **kwargs):
        super().__init__(**parse_with_information_dict(kwargs))


class UserProfile(ApiData):
    """This model represents profile of user, returned from the Boticord API"""

    id: str
    """Id of User"""

    status: str
    """Status of user"""

    badge: typing.Optional[str]
    """User's badge"""

    short_code: typing.Optional[str]
    """User's profile page short code"""

    site: typing.Optional[str]
    """User's website"""

    vk: typing.Optional[str]
    """User's VK Profile"""

    steam: typing.Optional[str]
    """User's steam account"""

    youtube: typing.Optional[str]
    """User's youtube channel"""

    twitch: typing.Optional[str]
    """User's twitch channel"""

    git: typing.Optional[str]
    """User's github/gitlab (or other git-service) profile"""

    def __init__(self, **kwargs):
        super().__init__(**parse_response_dict(kwargs))


class UserComments(ApiData):
    """This model represents all the user's comments on every page"""

    bots: list
    """Data from `get_bot_comments` method"""

    servers: list
    """Data from `get_server_comments` method"""

    def __init__(self, **kwargs):
        super().__init__(**parse_user_comments_dict(kwargs))


class SimpleBot(ApiData):
    """This model represents a short bot information (`id`, `short`).
    After that you can get more information about it using `get_bot_info` method."""

    id: str
    """Bot's Id"""

    short_code: typing.Optional[str]

    def __init__(self, **kwargs):
        super().__init__(**parse_response_dict(kwargs))


class CommentData(ApiData):
    """This model represents comment data (from webhook response)"""

    vote: dict
    old: typing.Optional[str]
    new: typing.Optional[str]

    def __init__(self, **kwargs):
        super().__init__(**parse_response_dict(kwargs))


def parse_webhook_response_dict(webhook_data: dict) -> dict:
    data = webhook_data.copy()

    for key, value in data.copy().items():
        if key.lower() == "data":
            for data_key, data_value in value.copy().items():
                if data_key == "comment":
                    data[data_key] = CommentData(**data_value)
                else:
                    converted_data_key = "".join(
                        ["_" + x.lower() if x.isupper() else x for x in data_key]
                    ).lstrip("_")

                    data[converted_data_key] = data_value

            del data["data"]
        else:
            data[key] = value

    return data


class BumpResponse(ApiData):
    """This model represents a webhook response (`bot bump`)."""

    type: str
    user: str
    at: int

    def __init__(self, **kwargs):
        super().__init__(**parse_webhook_response_dict(kwargs))


class CommentResponse(ApiData):
    """This model represents a webhook response (`comment`)."""

    type: str
    user: str
    comment: CommentData
    reason: typing.Optional[str]
    at: int

    def __init__(self, **kwargs):
        super().__init__(**parse_webhook_response_dict(kwargs))

