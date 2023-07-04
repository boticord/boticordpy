
# Migration Guide

You can use this guide to make it easier to switch to new version (3x) of boticordpy.

## Upgrading boticordpy
Run this command in terminal:

```pip install boticordpy --upgrade```

## BoticordClient
With a new BotiCord token system you don't need to specify type of token:

### Was:
```py
boticord_client = BoticordClient(
	"Bot your_api_token", version=2
)
```
### Became:
```py
boticord_client = BoticordClient(
	"your_api_token", version=3
)
```

You can get a new token in your account settings (not a bot's!)
![Get token here](https://i.ibb.co/wJM7DCq/image.png)

## Autoposting

Since the token is no longer connected to the bot you need to specify the ID when starting the autoposting:

### Was:
```py
autopost = (
    boticord_client.autopost()
    .init_stats(get_stats)
    .on_success(on_success_posting)
    .start()
)
```
### Became:
```py
autopost = (
    boticord_client.autopost()
    .init_stats(get_stats)
    .on_success(on_success_posting)
    .start("id_of_your_bot")  # <--- ID of your bot
)
```

Also, JSON's keys for bot stats must be changed:

### Was:
```py
async def get_stats():
    return {"servers": len(bot.guilds), "shards": 0, "users": len(bot.users)}
```

### Became:
```py
async def get_stats():
    return {"servers": len(bot.guilds), "shards": 0, "members": len(bot.users)}
```

## Webhook or websocket... that is the question

Webhooks are no longer supported in boticordpy. You can find guide how to use boticord websocket [here](https://github.com/boticord/boticordpy/blob/master/examples/websocket.py).

## Extra changes

There are some additional changes to the data models and new search methods added.
So, I recommend you to read [the docs](https://py.boticord.top/)