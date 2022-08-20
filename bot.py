#   BOT MADE BY AKEX06
#   https://github.com/akex06 <3

import discord

from discord.ext import commands
from discord import app_commands, errors

from src.constants import (
    TOKEN,
    DEFAULT_PREFIX
)

class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=DEFAULT_PREFIX,
            intents=discord.Intents.all()
        )

    async def on_ready(self) -> None:
        print(f"[   READY   ]: {self.user}")
        print(f"[   GUILDS   ]: {len(self.guilds)}")
        print(f"[   USERS   ]: {len(self.users)}")

    async def setup_hook(self) -> None:
        await self.load_extension("cogs.economy")
        await self.tree.sync()

    async def on_command_error(self, ctx, error) -> None:
        await ctx.reply(
            error,
            ephemeral = True
        )

bot = Bot()
bot.run(TOKEN)