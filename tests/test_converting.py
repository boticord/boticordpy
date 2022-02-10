import pytest

from boticordpy import types

single_comment_dict = {
    "userID": "525366699969478676",
    "text": "aboba",
    "vote": 1,
    "isUpdated": False,
    "createdAt": 1644388399
}

bot_data_dict = {
     "id": "724663360934772797",
     "shortCode": "kerdoku",
     "links": ["https://boticord.top/bot/724663360934772797",
               "https://bcord.cc/b/724663360934772797",
               "https://myservers.me/b/724663360934772797",
               "https://boticord.top/bot/kerdoku",
               "https://bcord.cc/b/kerdoku",
               "https://myservers.me/b/kerdoku"],
     "server": {
         "id": "724668798874943529",
         "approved": True
     },
     "information": {
         "bumps": 37,
         "added": 1091,
         "prefix": "?",
         "permissions": 1544023111,
         "tags": [
             "комбайн",
             "экономика",
             "модерация",
             "приветствия"
         ],
         "developers": ["585766846268047370"],
         "links": {
            "discord": "5qXgJvr",
            "github": None,
            "site": "https://kerdoku.top"
         },
         "library": "discordpy",
         "shortDescription": "Удобный и дружелюбный бот, который имеет крутой функционал!",
         "longDescription": "wow",
         "badge": None,
         "stats": {
             "servers": 2558,
             "shards": 3,
             "users": 348986
         },
         "status": "APPROVED"
     }
}

server_data_dict = {
   "id": "722424773233213460",
   "shortCode": "boticord",
   "status": "ACCEPT_MEMBERS",
   "links": [
      "https://boticord.top/server/722424773233213460",
      "https://bcord.cc/s/722424773233213460",
      "https://myservers.me/s/722424773233213460",
      "https://boticord.top/server/boticord",
      "https://bcord.cc/s/boticord",
      "https://myservers.me/s/boticord"
   ],
   "bot": {
      "id": None,
      "approved": False
   },
   "information": {
      "name": "BotiCord Community",
      "avatar": "https://cdn.discordapp.com/icons/722424773233213460/060188f770836697846710b109272e4c.webp",
      "members": [
         438,
         0
      ],
      "bumps": 62,
      "tags": [
         "аниме",
         "игры",
         "поддержка",
         "комьюнити",
         "сообщество",
         "discord",
         "дискорд сервера",
         "дискорд боты"
      ],
      "links": {
         "invite": "hkHjW8a",
         "site": "https://boticord.top/",
         "youtube": None,
         "twitch": None,
         "steam": None,
         "vk": None
      },
      "shortDescription": "short text",
      "longDescription": "long text",
      "badge": "STAFF"
   }
}

user_profile_dict = {
    "id": '178404926869733376',
    "status": '"Если вы не разделяете мою точку зрения, поздравляю — вам больше достанется." © Артемий Лебедев',
    "badge": 'STAFF',
    "shortCode": 'cipherka',
    "site": 'https://sqdsh.top/',
    "vk": None,
    "steam": 'sadlycipherka',
    "youtube": None,
    "twitch": None,
    "git": 'https://git.sqdsh.top/me'
}


@pytest.fixture
def single_comment() -> types.SingleComment:
    return types.SingleComment(**single_comment_dict)


@pytest.fixture
def bot_data() -> types.Bot:
    return types.Bot(**bot_data_dict)


@pytest.fixture
def server_data() -> types.Server:
    return types.Bot(**server_data_dict)


@pytest.fixture
def user_profile_data() -> types.UserProfile:
    return types.UserProfile(**user_profile_dict)


def test_comment_dict_fields(single_comment: types.SingleComment) -> None:
    for attr in single_comment:
        assert single_comment.get(attr) == getattr(single_comment, attr)


def test_user_profile_dict_fields(user_profile_data: types.UserProfile) -> None:
    for attr in user_profile_data:
        assert user_profile_data.get(attr) == getattr(user_profile_data, attr)


def test_bot_dict_fields(bot_data: types.Bot) -> None:
    for attr in bot_data:
        if attr.lower() == "information":
            assert bot_data["information"].get(attr) == getattr(bot_data, attr)
        else:
            assert bot_data[attr] == getattr(bot_data, attr)


def test_server_dict_fields(server_data: types.Server) -> None:
    for attr in server_data:
        if attr.lower() == "information":
            assert server_data["information"].get(attr) == getattr(bot_data, attr)
        else:
            assert server_data[attr] == getattr(server_data, attr)
