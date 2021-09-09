<h1 align="center">Boticordpy</h1>

<p align="center">Модуль для работы с <a href="https://boticord.top/">Boticord</a> API</p>

<p align="center">

<img src="https://img.shields.io/pypi/dm/boticordpy" alt="">
</p>

---
* [Документация](https://boticordpy.readthedocs.io/)
* [Исходный код](https://github.com/grey-cat-1908/boticordpy)
---

### Примеры

Публикуем статистику нашего бота в Boticord.

```Python
from discord.ext import commands

from boticordpy import BoticordClient

bot = commands.Bot(command_prefix="!")
boticord = BoticordClient(bot, "your-boticord-token")


@bot.event
async def on_ready():
    stats = {"servers": len(bot.guilds), "shards": bot.shard_count, "users": len(bot.users)}
    await boticord.Bots.postStats(stats)


bot.run("your-bot-token")
```
