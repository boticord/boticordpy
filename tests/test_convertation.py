from boticordpy import types


resource_up_dict = {"id": "arbuz123", "expires": "1685262170000"}
resource_rating_dict = {"count": 15, "rating": 5}
resource_bot_dict = {
    "id": "947141336451153931",
    "name": "BumpBot",
    "status": 1,
    "createdDate": "2023-05-22T22:29:23.264Z",
    "premium": {},
}
resource_server_dict = {
    "id": "722424773233213460",
    "name": "BotiCord.top",
    "tags": [134, 132],
    "status": 1,
    "createdDate": "2023-05-23T15:16:45.387Z",
    "premium": {},
}
user_profile_dict = {
    "id": "585766846268047370",
    "username": "Marakarka",
    "bots": [resource_bot_dict],
    "shortDescription": None,
}


def test_resource_up_convertation():
    model_from_dict = types.ResourceUp.from_dict(resource_up_dict)

    assert model_from_dict.id == "arbuz123"
    assert (
        model_from_dict.expires.strftime("%Y.%m.%d %H:%M:%S") == "2023.05.28 08:22:50"
    )

    dict_from_model = model_from_dict.to_dict()

    assert dict_from_model == resource_up_dict


def test_resource_rating_convertation():
    model_from_dict = types.ResourceRating.from_dict(resource_rating_dict)

    assert model_from_dict.count == 15
    assert model_from_dict.rating == 5

    dict_from_model = model_from_dict.to_dict()

    assert dict_from_model == resource_rating_dict


def test_resource_bot_convertation():
    model_from_dict = types.ResourceBot.from_dict(resource_bot_dict)

    assert int(model_from_dict.created_date.timestamp()) == 1684794563
    assert model_from_dict.status.name == "PUBLIC"


def test_resource_server_convertation():
    model_from_dict = types.ResourceServer.from_dict(resource_server_dict)

    assert int(model_from_dict.created_date.timestamp()) == 1684855005
    assert model_from_dict.name == "BotiCord.top"
    assert model_from_dict.tags[1].name == "GAMES"


def test_user_profile_convertation():
    model_from_dict = types.UserProfile.from_dict(user_profile_dict)

    assert model_from_dict.id == "585766846268047370"
    assert model_from_dict.username == "Marakarka"
    assert model_from_dict.short_description == None
    assert model_from_dict.bots[0].id == "947141336451153931"
