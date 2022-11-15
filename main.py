import asyncio
import logging
import logging.handlers
from typing import List

import discord
from discord.ext import commands

token = ""

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
prefix = "$"


class smallpop(commands.Bot):
    def __init__(self, initial_exts: List[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_exts = initial_exts

    async def setup_hook(self) -> None:
        for cog in self.initial_exts:
            await self.load_extension(cog)


async def main():
    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )

    discord.utils.setup_logging(handler=handler, root=False)
    exts = ['commands.fun']
    async with smallpop(initial_exts=exts, command_prefix=prefix, intents=intents) as bot:
        await bot.start(token=token)


asyncio.run(main())
