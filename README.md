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

#### Без Когов
Публикуем статистику при запуске бота.

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

#### С Когами

Ког с автоматической публикацией статистики раз в 15 минут + команда для публикации статистики для владельца бота.

```python
from discord.ext import commands

from boticordpy import BoticordClient


class BoticordCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.boticord = BoticordClient(self.bot, "your-boticord-token")
        self.boticord.start_loop()

    @commands.command(name="boticord-update")
    @commands.is_owner()
    async def boticord_update(self, ctx):
        """
            This commands can be used by owner to post stats to boticord
        """
        stats = {"servers": len(self.bot.guilds), "shards": 0, "users": len(self.bot.users)}
        await self.boticord.Bots.postStats(stats)


def setup(bot):
    bot.add_cog(BoticordCog(bot))

```
