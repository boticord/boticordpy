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
