import discord

from discord.ext import commands
from discord import app_commands

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


bot = Bot()
bot.run(TOKEN)