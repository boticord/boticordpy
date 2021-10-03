from aiohttp import ClientResponse

from disnake.ext import commands as commandsnake
from discord.ext import commands

from typing import Union
import json


from . import exceptions
from . import types


class Config:
    local_api = "https://boticord.top/api"
    general_api = "https://api.boticord.top/v1"
    http_exceptions = {401: exceptions.Unauthorized,
                       403: exceptions.Forbidden,
                       404: exceptions.NotFound,
                       429: exceptions.ToManyRequests,
                       500: exceptions.ServerError,
                       503: exceptions.ServerError}
    events_list = {
        "new_bot_comment": types.Comment,
        "edit_bot_comment": types.EditedComment,
        "delete_bot_comment": types.Comment,
        "new_bot_bump": types.BotVote
    }
    libs = {
        "discordpy": commands,
        "disnake": commandsnake
    }


async def _json_or_text(response: ClientResponse) -> Union[dict, str]:
    text = await response.text()
    if response.headers['Content-Type'] == 'application/json; charset=utf-8':
        return json.loads(text)
    return text
