import typing
from enum import IntEnum

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
    """Base class used to represent received data from the API."""

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
    """This model represents a bot, returned from the BotiCord API"""

    id: str
    """Bot's Id"""

    name: str
    """Bot's name"""

    shortDescription: str
    """Bot's short description"""

    description: str
    """Bot's long description"""

    avatar: typing.Optional[str]
    """Bot's avatar"""

    shortLink: typing.Optional[str]
    """Bot's page short code"""

    inviteLink: str
    """Bot's invite link"""

    premiumActive: bool
    """Bot's premium status"""

    premiumSplashURL: typing.Optional[str]
    """Bot's splash URL"""

    premiumAutoFetch: typing.Optional[bool]
    """Bot's auto fetch status"""

    standardBannerID: int
    """Bot's standart banner ID"""

    premiumBannerURL: typing.Optional[str]
    """Bot's premium banner URL"""

    owner: str
    """Bot's owner"""

    status: int
    """Bot's status"""

    prefix: str
    """Bot's prefix"""

    discriminator: str
    """Bot's discriminator (soon deprecated)"""

    createdDate: str
    """Bot's creation date"""

    supportServerInviteLink: typing.Optional[str]
    """Bot's support server"""

    library: typing.Optional[int]
    """Bot's library"""

    guilds: typing.Optional[int]
    """Bot's guilds count"""

    shards: typing.Optional[int]
    """Bot's shards count"""

    members: typing.Optional[int]
    """Bot's members count"""

    website: typing.Optional[str]
    """Bot's website"""

    upCount: int
    """Bot's up count"""

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
    """Bot's page short code"""

    def __init__(self, **kwargs):
        super().__init__(**parse_response_dict(kwargs))


class CommentData(ApiData):
    """This model represents comment data (from webhook response)"""

    vote: dict
    """Comment vote data"""

    old: typing.Optional[str]
    """Old content of the comment"""

    new: typing.Optional[str]
    """New content of the comment"""

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
    """Type of response (`bump`)"""

    user: str
    """Id of user who did the action"""

    at: int
    """Timestamp of the action"""

    def __init__(self, **kwargs):
        super().__init__(**parse_webhook_response_dict(kwargs))


class CommentResponse(ApiData):
    """This model represents a webhook response (`comment`)."""

    type: str
    """Type of response (`comment`)"""

    user: str
    """Id of user who did the action"""

    comment: CommentData
    """Information about the comment"""

    reason: typing.Optional[str]
    """Is comment deleted? so, why?"""

    at: int
    """Timestamp of the  action"""

    def __init__(self, **kwargs):
        super().__init__(**parse_webhook_response_dict(kwargs))


class LinkDomain(IntEnum):
    """Domain to short the link"""

    BCORD_CC = 1
    """``bcord.cc`` domain, default"""

    DISCORD_CAMP = 3
    """``discord.camp`` domain"""


class ShortedLink(ApiData):
    id: int
    """Id of shorted link"""

    code: str
    """Code of shorted link"""

    owner_i_d: str
    """Id of owner of shorted link"""

    domain: str
    """Domain of shorted link"""

    views: int
    """Link views count"""

    date: int
    """Timestamp of link creation moment"""

    def __init__(self, **kwargs):
        super().__init__(**parse_response_dict(kwargs))
